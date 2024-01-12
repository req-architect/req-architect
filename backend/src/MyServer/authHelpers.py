import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import wraps
from typing import Dict, Tuple
from uuid import uuid4, UUID
import requests

import jwt
from decouple import config
from requests_oauthlib import OAuth2Session
from rest_framework import status
from rest_framework.response import Response


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
        "scope": ["read_user", "read_repository", "write_repository"]
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
class OAuthRequestUserInfo:
    token: str
    provider: OAuthProvider
    uid: str
    userName: str
    userMail: str


tokenMap = TokenMap()


class AuthProviderAPI:
    def __init__(self, provider: OAuthProvider):
        self._provider = provider

    def create_access_token(self, request_uri: str):
        clientId, clientSecret = config(self._provider.name.upper() + "_CLIENT_ID"), config(
            self._provider.name.upper() + "_CLIENT_SECRET")
        redirect_uri = self._provider.get_redirect_url()
        session = OAuth2Session(clientId, redirect_uri=redirect_uri)
        session.fetch_token(PROVIDER_INFO[self._provider]["token_url"], client_secret=clientSecret,
                            authorization_response=request_uri)
        return OAuthTokenWithInfo(session.access_token,
                                  self._provider,
                                  session.token.get("refresh_token"),
                                  session.token.get("created_at"),
                                  session.token.get("expires_in"))
    
    def getUserMail(self, token):
        url = 'https://api.github.com/user/emails'
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)  
        if response.status_code == 200:
            emails = response.json()
            for email in emails:
                if email['primary'] and email['verified']:
                    return email['email']

    def get_identity(self, token: OAuthToken) -> Tuple[str, str]:
        session =  OAuth2Session(token={"access_token": token.token, "token_type":"Bearer"})
        if self._provider == OAuthProvider.GITHUB:
            r = session.get("https://api.github.com/user").json()
            email = self.getUserMail(token.token)
            return r['id'], r['login'], email
        else:
            r = session.get("https://gitlab.com/api/v4/user").json()
            return r['id'], r['username'], r['email']
        
    def get_repos(self, token: str):
        if self._provider == OAuthProvider.GITHUB:
            print("IN GITHUB REPOS")
            headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {token}',
            }
            url = 'https://api.github.com/user/repos'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                repositories = response.json()
                write_access_repos = [repo["full_name"] for repo in repositories if repo['permissions']['push']]
                return write_access_repos
            else:
                return None
        else:
            print(f"IN GITLAB REPOS, TOKEN: {token}")
            headers = {
                'PRIVATE-TOKEN': token,
            }
            url = 'https://gitlab.com/api/v4/projects?membership=true&min_access_level=40'
            response = requests.get(url, headers=headers)
            print(response)
            if response.status_code == 200:
                repositories = response.json()
                print(f"repos: {repositories}")
                repo_names = [repo["name"] for repo in repositories]
                # print(repo_names)
                return repo_names



def generate_frontend_redirect_url(request_uri: str, provider: AuthProviderAPI) -> str:
    token = provider.create_access_token(request_uri)  # handle exceptions
    uuid = tokenMap.insertToken(token)
    expiration_time_minutes = 30  # change later
    exp = (datetime.now(timezone.utc) + timedelta(minutes=expiration_time_minutes)).timestamp()
    iat = datetime.now(timezone.utc).timestamp()
    jwt_token = jwt.encode({"uuid": str(uuid), "exp": exp, "iat": iat}, config("JWT_SECRET"))
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
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        auth_type, token = authHeader.split(" ")[:2]
        if auth_type != "Bearer":
            return Response({'message': 'Wrong auth type'}, status=status.HTTP_401_UNAUTHORIZED)
        jwtToken = authHeader.split(" ")[1]
        try:
            payload = jwt.decode(jwtToken, config("JWT_SECRET"), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        oAuthToken = tokenMap.getToken(UUID(payload["uuid"]))
        if not oAuthToken:
            return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        uid, userName, email = AuthProviderAPI(oAuthToken.provider).get_identity(oAuthToken)
        oAuthRequestUserInfo = OAuthRequestUserInfo(oAuthToken.token, oAuthToken.provider, uid, userName, email)
        request.auth = oAuthRequestUserInfo
        return func(self, request, *args, **kwargs)

    return wrapper
