from datetime import datetime, timezone
import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from rest_framework import status
import jwt
from MyServer.authHelpers import (
    OAuthProvider,
    OAuthToken,
    TokenMap,
    AuthProviderAPI,
    generate_frontend_redirect_url,
    generate_authorization_url,
    requires_jwt_login,
)


class TestAuthHelpers(unittest.TestCase):
    @patch("MyServer.authHelpers.config")
    def test_get_redirect_url(self, mock_config):
        mock_config.side_effect = lambda key: {
            "BACKEND_URL": "https://backend.example.com",
        }[key]
        provider_github = OAuthProvider.GITHUB
        provider_gitlab = OAuthProvider.GITLAB
        self.assertTrue(
            provider_github.get_redirect_url().endswith("/MyServer/login_callback/github"),
        )
        self.assertTrue(
            provider_gitlab.get_redirect_url().endswith("/MyServer/login_callback/gitlab"),
        )

    @patch("MyServer.authHelpers.AuthProviderAPI.get_identity")
    @patch("MyServer.authHelpers.config")
    @patch("MyServer.authHelpers.uuid4")
    @patch("MyServer.authHelpers.datetime")
    @patch("MyServer.authHelpers.OAuth2Session")
    def test_generate_frontend_redirect_url(self, mock_session, mock_datetime, mock_uuid4, mock_config, mock_get_identity):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc)
        mock_uuid4.return_value = "mocked_uuid"
        mock_config.side_effect = lambda key: {
            "GITHUB_CLIENT_ID": "mocked_client_id",
            "GITHUB_CLIENT_SECRET": "mocked_client_secret",
            "FRONTEND_URL": "https://example.com",
            "JWT_SECRET": "mocked_jwt_secret",
            "BACKEND_URL": "https://backend.example.com",
        }[key]

        mock_session_instance = mock_session.return_value
        mock_session_instance.fetch_token.return_value = {"access_token": "mocked_access_token"}
        mock_get_identity.return_value = ("mocked_uid", "mocked_user_name", "mocked_user_mail")

        redirect_url = generate_frontend_redirect_url("/callback", AuthProviderAPI(OAuthProvider.GITHUB))

        mock_session.assert_called_once_with("mocked_client_id", redirect_uri="https://backend.example.com/MyServer/login_callback/github")
        mock_session_instance.fetch_token.assert_called_once_with(
            "https://github.com/login/oauth/access_token", client_secret="mocked_client_secret", authorization_response="/callback"
        )
        mock_get_identity.assert_called_once()
        self.assertTrue(redirect_url.startswith("https://example.com/login_callback?token="))

    @patch("MyServer.authHelpers.config")
    def test_generate_authorization_url_github(self, mock_config):
        mock_config.return_value = "https://backend.example.com"
        authorization_url = generate_authorization_url(OAuthProvider.GITHUB)
        mock_config.assert_called_with("BACKEND_URL")
        self.assertTrue(authorization_url.startswith("https://github.com/login/oauth/authorize"))

    @patch("MyServer.authHelpers.config")
    def test_generate_authorization_url_gitlab(self, mock_config):
        mock_config.return_value = "https://backend.example.com"
        authorization_url = generate_authorization_url(OAuthProvider.GITLAB)
        mock_config.assert_called_with("BACKEND_URL")
        self.assertTrue(authorization_url.startswith("https://gitlab.com/oauth/authorize"))

    @patch("MyServer.authHelpers.config")
    @patch("MyServer.authHelpers.jwt.decode")
    @patch("MyServer.authHelpers.tokenMap.getToken")
    def test_requires_jwt_login_valid_token(self, mock_get_token, mock_jwt_decode, mock_config):
        valid_jwt_token = "valid_jwt_token"
        valid_uuid = UUID("550e8400-e29b-41d4-a716-446655440000")
        valid_oauth_token = OAuthToken("valid_token", OAuthProvider.GITHUB)
        mock_config.side_effect = lambda key: {
            "JWT_SECRET": "mocked_jwt_secret",
        }[key]

        mock_jwt_decode.side_effect = lambda *args, **kwargs: {"uuid": str(valid_uuid), "user_id": "mocked_uid"}

        mock_get_token.return_value = valid_oauth_token

        @requires_jwt_login
        def dummy_view(self, request):
            return "OK"

        test_instance = TestAuthHelpers()
        request = MagicMock()
        request.headers = {"Authorization": "Bearer " + valid_jwt_token}
        response = dummy_view(test_instance, request)

        mock_jwt_decode.assert_called_once_with(valid_jwt_token, "mocked_jwt_secret", algorithms=["HS256"])
        mock_get_token.assert_called_once_with(valid_uuid)
        self.assertEqual(request.auth.token, valid_oauth_token.token)
        self.assertEqual(response, "OK")

    def test_requires_jwt_login_no_auth_header(self):
        @requires_jwt_login
        def dummy_view(self, request, *args, **kwargs):
            return "OK"

        request = MagicMock()
        request.headers = {}
        response = dummy_view(self, request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "Unauthorized"})

    def test_requires_jwt_login_wrong_auth_type(self):
        @requires_jwt_login
        def dummy_view(self, request, *args, **kwargs):
            return "OK"

        request = MagicMock()
        request.headers = {"Authorization": "Basic some_credentials"}
        response = dummy_view(self, request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "Wrong auth type"})

    @patch("MyServer.authHelpers.config")
    def test_requires_jwt_login_expired_token(self, mock_config):
        mock_config.side_effect = lambda key: {
            "JWT_SECRET": "mocked_jwt_secret",
        }[key]

        @requires_jwt_login
        def dummy_view(self, request, *args, **kwargs):
            return "OK"

        with patch("MyServer.authHelpers.jwt.decode", side_effect=jwt.ExpiredSignatureError):
            request = MagicMock()
            request.headers = {"Authorization": "Bearer expired_jwt_token"}
            response = dummy_view(self, request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "Token expired"})

    @patch("MyServer.authHelpers.jwt.decode")
    @patch("MyServer.authHelpers.tokenMap.getToken")
    @patch("MyServer.authHelpers.config")
    def test_requires_jwt_login_invalid_token(self, mock_config, mock_get_token, mock_jwt_decode):
        mock_config.side_effect = lambda key: {
            "JWT_SECRET": "mocked_jwt_secret",
        }[key]

        @requires_jwt_login
        def dummy_view(self, request, *args, **kwargs):
            return "OK"

        valid_uuid_UUID = UUID("550e8400-e29b-41d4-a716-446655440000")
        valid_uuid = str(valid_uuid_UUID)
        mock_jwt_decode.return_value = {"uuid": valid_uuid}

        mock_get_token.return_value = None

        request = MagicMock()
        request.headers = {"Authorization": "Bearer invalid_jwt_token"}
        response = dummy_view(self, request)

        mock_config.assert_called_once()
        mock_jwt_decode.assert_called_once()
        mock_get_token.assert_called_once_with(valid_uuid_UUID)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "Invalid token"})

    def test_getToken_found(self):
        token_map = TokenMap()
        existing_uuid = uuid4()
        existing_token = OAuthToken("mocked_token", OAuthProvider.GITHUB)
        token_map._tokenDict[existing_uuid] = existing_token
        result = token_map.getToken(existing_uuid)
        self.assertEqual(result, existing_token)

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_getUserMail_github(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"email": "test@example.com", "primary": True, "verified": True}]
        mock_requests_get.return_value = mock_response

        auth_provider = AuthProviderAPI(OAuthProvider.GITHUB)
        email = auth_provider.getUserMail("mocked_token")

        mock_requests_get.assert_called_once_with("https://api.github.com/user/emails")
        mock_requests_get.return_value.json.assert_called_once()
        self.assertEqual(email, "test@example.com")

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_getUserMail_gitlab(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"email": "test@example.com", "primary": True, "verified": True}]
        mock_requests_get.return_value = mock_response

        auth_provider = AuthProviderAPI(OAuthProvider.GITLAB)
        email = auth_provider.getUserMail("mocked_token")

        mock_requests_get.assert_called_once_with("https://gitlab.com/api/v4/user/emails")
        mock_requests_get.return_value.json.assert_called_once()
        self.assertEqual(email, "test@example.com")

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_getUserMail_github_status_code_400(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 400

        auth_provider = AuthProviderAPI(OAuthProvider.GITHUB)
        self.assertRaises(Exception, auth_provider.getUserMail, "mocked_token")
        mock_requests_get.assert_called_once_with("https://api.github.com/user/emails")

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_getUserMail_gitlab_no_valid_email(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_requests_get.return_value = mock_response

        auth_provider = AuthProviderAPI(OAuthProvider.GITLAB)
        email = auth_provider.getUserMail("mocked_token")
        self.assertIsNone(email)

        mock_response.json.return_value = [{"email": "test@example.com", "primary": False, "verified": False}]
        email = auth_provider.getUserMail("mocked_token")
        self.assertIsNone(email)

        mock_response.json.return_value = [
            {"email": "test@example.com", "primary": True, "verified": False},
            {"email": "test2@example.com", "primary": False, "verified": True},
        ]
        email = auth_provider.getUserMail("mocked_token")
        self.assertIsNone(email)

    @patch("MyServer.authHelpers.OAuth2Session.get")
    @patch("MyServer.authHelpers.OAuth2Session")
    def test_get_identity_github(self, mock_oauth_session, mock_requests_get):
        mock_oauth_session_instance = mock_oauth_session.return_value
        mock_oauth_session_instance.get.return_value.json.return_value = {"id": "mocked_id", "login": "mocked_login", "email": "mocked_email"}
        mock_requests_get.return_value.status_code = 200

        auth_provider = AuthProviderAPI(OAuthProvider.GITHUB)
        token = OAuthToken("mocked_token", OAuthProvider.GITHUB)
        identity = auth_provider.get_identity(token)

        mock_oauth_session.assert_called_once_with(token={"access_token": token, "token_type": "Bearer"})
        mock_oauth_session_instance.get.assert_called_once_with("https://api.github.com/user")
        self.assertEqual(identity, ("mocked_id", "mocked_login", "mocked_email"))

    @patch("MyServer.authHelpers.OAuth2Session")
    def test_get_identity_gitlab(self, mock_oauth_session):
        mock_oauth_session_instance = mock_oauth_session.return_value
        mock_oauth_session_instance.get.return_value.json.return_value = {"id": "mocked_id", "username": "mocked_login", "email": "mocked_email"}

        auth_provider = AuthProviderAPI(OAuthProvider.GITLAB)
        token = OAuthToken("mocked_token", OAuthProvider.GITLAB)
        identity = auth_provider.get_identity(token)

        mock_oauth_session.assert_called_once_with(token={"access_token": token, "token_type": "Bearer"})
        mock_oauth_session_instance.get.assert_called_once_with("https://gitlab.com/api/v4/user")
        self.assertEqual(identity, ("mocked_id", "mocked_login", "mocked_email"))

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_get_repos_github(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"full_name": "user/repo1", "permissions": {"push": True}},
            {"full_name": "user/repo2", "permissions": {"push": False}},
        ]
        mock_requests_get.return_value = mock_response

        auth_provider = AuthProviderAPI(OAuthProvider.GITHUB)
        repos = auth_provider.get_repos("mocked_token")

        mock_requests_get.assert_called_once_with("https://api.github.com/user/repos", headers={"Accept": "application/vnd.github+json"})
        mock_response.json.assert_called_once()
        self.assertEqual(repos, ["user/repo1"])

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_get_repos_gitlab(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"path_with_namespace": "project1"}, {"path_with_namespace": "project2"}]
        mock_requests_get.return_value = mock_response

        auth_provider = AuthProviderAPI(OAuthProvider.GITLAB)
        repos = auth_provider.get_repos("mocked_token")

        mock_requests_get.assert_called_once_with("https://gitlab.com/api/v4/projects?membership=true&min_access_level=40")
        mock_response.json.assert_called_once()
        self.assertEqual(repos, ["project1", "project2"])

    @patch("MyServer.authHelpers.OAuth2Session.get")
    def test_get_repos_github_status_401(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_requests_get.return_value = mock_response

        auth_provider = AuthProviderAPI(OAuthProvider.GITHUB)
        repos = auth_provider.get_repos("mocked_token")

        mock_requests_get.assert_called_once_with("https://api.github.com/user/repos", headers={"Accept": "application/vnd.github+json"})
        self.assertIsNone(repos)
