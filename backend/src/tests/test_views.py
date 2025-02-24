from functools import wraps
from unittest.mock import patch, ANY


def mock_requires_jwt_login(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        request.auth = AuthInfo("test_token", OAuthProvider.GITLAB, "test_id")
        return func(self, request, *args, **kwargs)

    return wrapper


patch("api.authHelpers.requires_jwt_login", mock_requires_jwt_login).start()
import json
from django.http import JsonResponse
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
import rest_framework
import api.views as views
from rest_framework.test import APIRequestFactory
from django.http import HttpResponseRedirect
from api.authHelpers import AuthProviderAPI, OAuthProvider, AuthInfo
from oauthlib.oauth2 import AccessDeniedError


class TestViews(SimpleTestCase):
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.restHandlersHelpers.delete_user_requirement")
    def test_ReqView_DELETE(self, mock_delete_user_requirement, mock_repo_info, mock_get_repos_from_file):
        mock_delete_user_requirement.return_value = True
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"

        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.data["message"], "OK")
        mock_delete_user_requirement.assert_called_once_with(data["docId"], data["reqId"], "repo_folder/req")
        mock_repo_info.assert_called_once()
        mock_get_repos_from_file.assert_called_once()

    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    def test_ReqView_DELETE_ServerProblem(self, mock_get_repo_info, mock_get_repos_from_file):
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
        mock_get_repo_info.assert_called_once()
        mock_get_repos_from_file.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.edit_user_requirement")
    def test_ReqView_PUT(self, mock_edit_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_edit_user_requirement.return_value = True
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
            "reqText": "your_req_text",
        }
        edit_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.put(edit_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.data["message"], "OK")
        mock_edit_user_requirement.assert_called_once_with(data["docId"], data["reqId"], data["reqText"], "repo_folder/req")
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.add_user_requirement")
    def test_ReqView_POST(self, mock_add_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_add_user_requirement.return_value = True
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqNumberId": "your_req_id",
            "reqText": "your_req_text",
        }
        add_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.post(add_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.data["message"], "OK")
        mock_add_user_requirement.assert_called_once_with(data["docId"], data["reqNumberId"], data["reqText"], "repo_folder/req")
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.serialize_doc_reqs")
    @patch("api.restHandlersHelpers.get_doc_reqs")
    def test_ReqView_GET(self, mock_get_user_requirement, mock_serialize_doc_reqs, mock_get_repos_from_file, mock_repo_info):
        mock_get_user_requirement.return_value = ["req1", "req2"]
        mock_serialize_doc_reqs.return_value = [{"id": "1", "text": "Req 1", "reviewed": True, "links": ["link1", "link2"]}]
        data = {"docId": "your_doc_id"}
        url = reverse("req") + f'?docId={data["docId"]}'
        response = self.client.get(url)

        mock_get_user_requirement.assert_called_once_with("your_doc_id", "repo_folder/req")
        mock_serialize_doc_reqs.assert_called_once_with(["req1", "req2"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'[{"id": "1", "text": "Req 1", "reviewed": true, "links": ["link1", "link2"]}]')
        self.assertEqual(type(response), JsonResponse)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    def test_ReqView_GET_ServerProblem(self, mock_get_repos_from_file):
        url = reverse("req")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_get_repos_from_file.assert_called_once()

    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    def test_ReqView_GET_noDocId(self, mock_get_repos_from_file):
        url = reverse("req")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_get_repos_from_file.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.get_doc_reqs")
    def test_ReqView_GET_noReqs(self, mock_get_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_get_user_requirement.return_value = None
        data = {"docId": "your_doc_id"}
        url = reverse("req") + f'?docId={data["docId"]}'
        response = self.client.get(url)

        mock_get_user_requirement.assert_called_once_with("your_doc_id", "repo_folder/req")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"[]")
        self.assertEqual(type(response), JsonResponse)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.serialize_documents")
    def test_DocView_GET(self, mock_get_doc_reqs, mock_get_repos_from_file, mock_repo_info):
        mock_get_doc_reqs.return_value = ["doc1", "doc2"]
        url = reverse("doc")
        response = self.client.get(url)

        mock_get_doc_reqs.assert_called_once_with("repo_folder/req")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'["doc1", "doc2"]')
        self.assertEqual(type(response), JsonResponse)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.add_user_document", return_value=True)
    def test_DocView_POST(self, mock_add_user_document, mock_get_repos_from_file, mock_repo_info):
        url = reverse("doc")
        data = {
            "docId": "your_doc_id",
            "parentId": "parent",
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")

        mock_add_user_document.assert_called_once_with(data["docId"], data["parentId"], "repo_folder/req")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"message":"OK"}')
        self.assertEqual(type(response), rest_framework.response.Response)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.delete_user_document", return_value=True)
    def test_DocView_DELETE(self, mock_delete_document, mock_get_repos_from_file, mock_repo_info):
        url = reverse("doc")
        data = {
            "docId": "your_doc_id",
        }
        response = self.client.delete(url, data=json.dumps(data), content_type="application/json")

        mock_delete_document.assert_called_once_with(data["docId"], "repo_folder/req")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"message":"OK"}')
        self.assertEqual(type(response), rest_framework.response.Response)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.add_user_link", return_value=True)
    def test_LinkView_PUT(self, mock_link, mock_get_repos_from_file, mock_repo_info):
        url = reverse("linkView")
        data = {
            "req1Id": "my_req1Id",
            "req2Id": "my_req2Id",
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        mock_link.assert_called_once_with(data["req1Id"], data["req2Id"], "repo_folder/req")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"message":"OK"}')
        self.assertEqual(type(response), rest_framework.response.Response)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.delete_user_link", return_value=True)
    def test_UnlinkView_PUT(self, mock_unlink, mock_get_repos_from_file, mock_repo_info):
        url = reverse("unlinkView")
        data = {
            "req1Id": "my_req1Id",
            "req2Id": "my_req2Id",
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        mock_unlink.assert_called_once_with(data["req1Id"], data["req2Id"], "repo_folder/req")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"message":"OK"}')
        self.assertEqual(type(response), rest_framework.response.Response)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()

    @patch("api.authHelpers.generate_frontend_redirect_url")
    def test_LoginCallbackView_GET(self, mock_generate_redirect_url):
        mock_generate_redirect_url.return_value = "http://example.com/callback"
        url = reverse("gitlabLoginCallbackView", kwargs={"provider_str": "gitlab"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "http://example.com/callback")
        self.assertEqual(type(response), HttpResponseRedirect)
        mock_generate_redirect_url.assert_called_once_with("http://testserver/api/login_callback/gitlab/", ANY)
        actual_argument = mock_generate_redirect_url.call_args[0][1]
        self.assertIsInstance(actual_argument, AuthProviderAPI)

    @patch("api.authHelpers.generate_frontend_redirect_url")
    def test_LoginCallbackView_GET_AccessDenied(self, mock_generate_redirect_url):
        mock_generate_redirect_url.side_effect = AccessDeniedError
        url = reverse("gitlabLoginCallbackView", kwargs={"provider_str": "gitlab"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("api.authHelpers.generate_authorization_url")
    def test_LoginView_GET(self, mock_generate_auth_url):
        mock_generate_auth_url.return_value = "http://example.com/authorization"
        provider_str = "gitlab"
        url = reverse("gitlabLoginView", kwargs={"provider_str": provider_str})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "http://example.com/authorization")
        mock_generate_auth_url.assert_called_once_with(OAuthProvider["GITLAB"])

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.get_all_reqs")
    @patch("api.restHandlersHelpers.serialize_all_reqs")
    def test_allReqsView_GET(self, mock_serial, mock_get_reqs, mock_get_repos_from_file, mock_repo_info):
        mock_get_reqs.return_value = ["req1", "req2"]
        url = reverse("allReqsView")
        mock_serial.return_value = [{"id": "1", "text": "Req 1", "reviewed": True, "links": ["link1", "link2"]}]
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'[{"id": "1", "text": "Req 1", "reviewed": true, "links": ["link1", "link2"]}]')
        self.assertEqual(type(response), JsonResponse)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()
        mock_get_reqs.assert_called_once_with("repo_folder/req")
        mock_serial.assert_called_once_with(["req1", "req2"])

    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.restHandlersHelpers.get_all_reqs")
    def test_allReqsView_GET_noReqs(self, mock_get_reqs, mock_get_repos_from_file, mock_repo_info):
        mock_get_reqs.return_value = []
        url = reverse("allReqsView")
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"[]")
        self.assertEqual(type(response), JsonResponse)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()
        mock_get_reqs.assert_called_once_with("repo_folder/req")

    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.authHelpers.AuthProviderAPI.get_identity")
    @patch("api.repoHelpers.stage_changes", return_value=True)
    def test_GitCommitView_POST(self, mock_stage, mock_get_identity, mock_get_repos_from_file, mock_repo_info):
        url = reverse("commitInRepo")
        data = {"commitText": "Test commit"}
        factory = APIRequestFactory()
        request = factory.post(url, data=data)
        mock_get_identity.return_value = ("test_id", "test_username", "test_email")
        view = views.GitCommitView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()
        mock_get_identity.assert_called_once_with(request.auth.token)
        mock_stage.assert_called_once_with("repo_folder", data["commitText"], "test_username", "test_email")

    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.authHelpers.AuthProviderAPI.get_identity")
    @patch("api.repoHelpers.stage_changes", return_value=True)
    @patch("api.authHelpers.AuthProviderAPI.get_user_mail")
    def test_GitCommitView_POST_noMail(self, mock_mail, mock_stage, mock_get_identity, mock_get_repos_from_file, mock_repo_info):
        url = reverse("commitInRepo")
        data = {"commitText": "Test commit"}
        factory = APIRequestFactory()
        request = factory.post(url, data=data)
        mock_get_identity.return_value = ("test_id", "test_username", None)
        mock_mail.return_value = "test_email"
        view = views.GitCommitView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()
        mock_get_identity.assert_called_once_with(request.auth.token)
        mock_stage.assert_called_once_with("repo_folder", data["commitText"], "test_username", "test_email")

    @patch("api.repoHelpers.get_repos_from_file", return_value={"repo_name": "repo_url"})
    @patch("api.repoHelpers.get_repo_info", return_value=("repo_folder", "repo_name"))
    @patch("api.authHelpers.AuthProviderAPI.get_identity")
    @patch("api.repoHelpers.stage_changes", return_value=False)
    def test_GitCommitView_POST_cantStage(self, mock_stage, mock_get_identity, mock_get_repos_from_file, mock_repo_info):
        url = reverse("commitInRepo")
        data = {"commitText": "Test commit"}
        factory = APIRequestFactory()
        request = factory.post(url, data=data)
        mock_get_identity.return_value = ("test_id", "test_username", "test_email")
        view = views.GitCommitView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        mock_get_repos_from_file.assert_called_once()
        mock_repo_info.assert_called_once()
        mock_get_identity.assert_called_once_with(request.auth.token)
        mock_stage.assert_called_once_with("repo_folder", data["commitText"], "test_username", "test_email")
