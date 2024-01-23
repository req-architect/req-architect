"""This module provides functions, data strucures and classes responsible for users authentication."""

import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import wraps
from typing import Dict, Tuple
from uuid import uuid4, UUID

import jwt
import requests
from decouple import config
from requests_oauthlib import OAuth2Session
from rest_framework import status
from rest_framework.response import Response
from oauthlib.oauth2 import InvalidGrantError

# for integrations tests
from MyServer.testHelpers import server_test_mode, MockedAuthInfo, TEST_USERNAME, TEST_UID, TEST_MAIL, TEST_TOKEN, TEST_REPOS
from MyServer.error import TokenNotPresentException, InvalidTokenException, OAuthProviderCommunicationException, InvalidAuthorizationCodeException


class OAuthProvider(Enum):
    GITHUB = 0
    GITLAB = 1

    def get_redirect_url(self) -> str:
        return config("BACKEND_URL") + "/MyServer/login_callback/" + self.name.lower()


PROVIDER_INFO: Dict[OAuthProvider, Dict[str, str]] = {
    OAuthProvider.GITHUB: {
        "authorization_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "scope": ["repo", "user:email", "read:user"]
    },
    OAuthProvider.GITLAB: {
        "authorization_url": "https://gitlab.com/oauth/authorize",
        "token_url": "https://gitlab.com/oauth/token",
        "scope": ["read_user", "read_repository", "write_repository", "read_api"]
    }
}


@dataclass
class OAuthToken:
    token: str
    provider: OAuthProvider


@dataclass
class OAuthTokenWithInfo(OAuthToken):
    refreshToken: str | None
    createdAt: int | None
    expiresIn: int | None


class TokenMap:
    def __init__(self):
        self._tokenDict: Dict[UUID, OAuthTokenWithInfo] = {}

    def insertToken(self, token: OAuthTokenWithInfo) -> UUID:
        uuid = uuid4()
        self._tokenDict[uuid] = token
        return uuid

    def getToken(self, uuid: UUID) -> OAuthTokenWithInfo | None:
        return self._tokenDict.get(uuid)


@dataclass
class AuthInfo:
    token: str
    provider: OAuthProvider
    uid: str


tokenMap = TokenMap()


def session_get_with_catch(session: OAuth2Session, *args, **kwargs):
    try:
        response = session.get(*args, **kwargs)
    except requests.ConnectionError:
        raise OAuthProviderCommunicationException
    if not response.ok:
        raise OAuthProviderCommunicationException
    return response


class AuthProviderAPI:
    def __init__(self, provider: OAuthProvider):
        self._provider = provider

    def create_access_token(self, request_uri: str):
        clientId, clientSecret = config(self._provider.name.upper() + "_CLIENT_ID"), config(
            self._provider.name.upper() + "_CLIENT_SECRET")
        redirect_uri = self._provider.get_redirect_url()
        session = OAuth2Session(clientId, redirect_uri=redirect_uri)
        try:
            session.fetch_token(PROVIDER_INFO[self._provider]["token_url"], client_secret=clientSecret,
                            authorization_response=request_uri)
        except InvalidGrantError:
            raise InvalidAuthorizationCodeException()
        except requests.ConnectionError:
            raise OAuthProviderCommunicationException(redirect=True)
        return OAuthTokenWithInfo(session.access_token,
                                  self._provider,
                                  session.token.get("refresh_token"),
                                  session.token.get("created_at"),
                                  session.token.get("expires_in"))

    def getUserMail(self, token_str: str) -> str | None:
        if server_test_mode():
            return TEST_MAIL

        session = OAuth2Session(token={"access_token": token_str, "token_type": "Bearer"})
        if self._provider == OAuthProvider.GITHUB:
            r = session_get_with_catch(session, 'https://api.github.com/user/emails')
        else:
            r = session_get_with_catch(session, 'https://gitlab.com/api/v4/user/emails')
        emails = r.json()
        for email in emails:
            if email['primary'] and email['verified']:
                return email['email']
        return None

    def get_identity(self, token_str: str) -> Tuple[str, str, str | None]:
        if server_test_mode():
            return TEST_UID, TEST_USERNAME, TEST_MAIL

        session = OAuth2Session(token={"access_token": token_str, "token_type": "Bearer"})
        if self._provider == OAuthProvider.GITHUB:
            r = session_get_with_catch(session, "https://api.github.com/user")
            identity = r.json()
            return identity['id'], identity['login'], identity['email']
        else:
            r = session_get_with_catch(session, "https://gitlab.com/api/v4/user")
            identity = r.json()
            return identity['id'], identity['username'], identity['email']

    def get_repos(self, token_str: str) -> list[str] | None:
        if server_test_mode():
            return TEST_REPOS

        session = OAuth2Session(token={"access_token": token_str, "token_type": "Bearer"})
        if self._provider == OAuthProvider.GITHUB:
            r = session_get_with_catch(session, 'https://api.github.com/user/repos', headers={
                'Accept': 'application/vnd.github+json'
            })
            repositories = r.json()
            write_access_repos = [repo["full_name"] for repo in repositories if repo['permissions']['push']]
            return write_access_repos
        else:
            r = session_get_with_catch(session, 'https://gitlab.com/api/v4/projects?membership=true&min_access_level=40')
            repositories = r.json()
            repo_names = [repo["path_with_namespace"] for repo in repositories]
            return repo_names


def generate_frontend_redirect_url(request_uri: str, provider: AuthProviderAPI) -> str:
    token = provider.create_access_token(request_uri)  # handle exceptions
    user_id, _, _ = provider.get_identity(token.token)
    uuid = tokenMap.insertToken(token)
    expiration_time_minutes = 30  # change later
    exp = (datetime.now(timezone.utc) + timedelta(minutes=expiration_time_minutes)).timestamp()
    iat = datetime.now(timezone.utc).timestamp()
    jwt_token = jwt.encode({"uuid": str(uuid), "exp": exp, "iat": iat, "user_id": user_id}, config("JWT_SECRET"))
    return config("FRONTEND_URL") + "/login_callback?" + urllib.parse.urlencode({
        "token": jwt_token,
        "exp": exp,
        "iat": iat,
    })


def generate_authorization_url(provider: OAuthProvider) -> str:
    clientId = config(provider.name.upper() + "_CLIENT_ID")
    redirect_uri = provider.get_redirect_url()
    session = OAuth2Session(clientId, redirect_uri=redirect_uri, scope=PROVIDER_INFO[provider]["scope"])
    authorization_url, state = session.authorization_url(PROVIDER_INFO[provider]["authorization_url"])
    return authorization_url


def requires_jwt_login(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        authHeader = request.headers.get("Authorization")
        if not authHeader:
            raise TokenNotPresentException()
        auth_type, token = authHeader.split(" ")[:2]
        if auth_type != "Bearer":
            raise TokenNotPresentException()
        jwtToken = authHeader.split(" ")[1]
        try:
            payload = jwt.decode(jwtToken, config("JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Token expired.")
        except jwt.InvalidSignatureError:
            raise InvalidTokenException("Token is invalid.")
        except jwt.DecodeError:
            raise InvalidTokenException("Token could not be decoded.")
        oAuthToken = tokenMap.getToken(UUID(payload["uuid"]))
        if not oAuthToken:
            raise InvalidTokenException("Token could not be verified.")
        user_id = payload["user_id"]
        authInfo = AuthInfo(oAuthToken.token, oAuthToken.provider, user_id)
        request.auth = authInfo
        return func(self, request, *args, **kwargs)

    @wraps(func)
    def test_wrapper(self, request, *args, **kwargs):
        request.auth = MockedAuthInfo(OAuthProvider.GITHUB)
        return func(self, request, *args, **kwargs)

    if server_test_mode():
        return test_wrapper
    return wrapper
