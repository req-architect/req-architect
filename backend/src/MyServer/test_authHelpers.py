from datetime import datetime, timezone
import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from rest_framework import status
import jwt
from MyServer.authHelpers import (
    OAuthProvider,
    PROVIDER_INFO,
    OAuthToken,
    TokenMap,
    AuthProviderAPI,
    generate_frontend_redirect_url,
    generate_authorization_url,
    requires_jwt_login,
)


class TestAuthHelpers(unittest.TestCase):
    def test_get_redirect_url(self):
        provider_github = OAuthProvider.GITHUB
        provider_gitlab = OAuthProvider.GITLAB
        self.assertTrue(
            provider_github.get_redirect_url().endswith("/MyServer/login_callback/github"),
        )
        self.assertTrue(
            provider_gitlab.get_redirect_url().endswith("/MyServer/login_callback/gitlab"),
        )

    @patch("MyServer.authHelpers.config")
    @patch("MyServer.authHelpers.uuid4")
    @patch("MyServer.authHelpers.datetime")
    @patch("MyServer.authHelpers.OAuth2Session")
    def test_generate_frontend_redirect_url(self, mock_session, mock_datetime, mock_uuid4, mock_config):
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

        redirect_url = generate_frontend_redirect_url("/callback", AuthProviderAPI(OAuthProvider.GITHUB))

        mock_session.assert_called_once_with("mocked_client_id", redirect_uri="https://backend.example.com/MyServer/login_callback/github")
        mock_session_instance.fetch_token.assert_called_once_with("https://github.com/login/oauth/access_token", client_secret="mocked_client_secret", authorization_response="/callback")
        self.assertTrue(redirect_url.startswith("https://example.com/login_callback?token="))

    @patch("MyServer.authHelpers.config")
    def test_generate_authorization_url_github(self, mock_config):
        mock_config.return_value = "https://backend.example.com"

        authorization_url = generate_authorization_url(OAuthProvider.GITHUB)

        mock_config.assert_called_with("BACKEND_URL")
        self.assertTrue(authorization_url.startswith("https://github.com/login/oauth/authorize"))

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

        mock_jwt_decode.side_effect = lambda *args, **kwargs: {"uuid": str(valid_uuid)}

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
        self.assertEqual(request.auth, valid_oauth_token)
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

        valid_uuid = str(UUID("550e8400-e29b-41d4-a716-446655440000"))
        mock_jwt_decode.return_value = {"uuid": valid_uuid}

        mock_get_token.return_value = None

        request = MagicMock()
        request.headers = {"Authorization": "Bearer invalid_jwt_token"}
        response = dummy_view(self, request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "Invalid token"})

    def test_getToken_found(self):
        token_map = TokenMap()

        existing_uuid = uuid4()
        existing_token = OAuthToken("mocked_token", OAuthProvider.GITHUB)

        token_map._tokenDict[existing_uuid] = existing_token

        result = token_map.getToken(existing_uuid)

        self.assertEqual(result, existing_token)
