from unittest.mock import patch

patch("MyServer.authHelpers.requires_jwt_login", lambda x: x).start()
import json
from django.http import JsonResponse
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status


class TestViews(SimpleTestCase):
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.restHandlersHelpers.deleteUserRequirement")
    def test_deleteRequirement(self, mock_delete_user_requirement, mock_repo_info, mock_get_repos_from_file):
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
        mock_delete_user_requirement.assert_called_once_with(data["docId"], data["reqId"], "repo_folder")

    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    def test_deleteRequirement_ServerProblem(self, mock_get_repo_info, mock_get_repos_from_file):
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.deleteUserRequirement")
    def test_deleteRequirement_cantBuild(self, mock_delete_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_delete_user_requirement.return_value = False
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.editUserRequirement")
    def test_editRequirement(self, mock_edit_user_requirement, mock_get_repos_from_file, mock_repo_info):
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
        mock_edit_user_requirement.assert_called_once_with(data["docId"], data["reqId"], data["reqText"], "repo_folder")

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.editUserRequirement")
    def test_editRequirement_canBuild(self, mock_edit_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_edit_user_requirement.return_value = False
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
            "reqText": "your_req_text",
        }

        edit_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.put(edit_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.addUserRequirement")
    def test_addRequirement(self, mock_add_user_requirement, mock_get_repos_from_file, mock_repo_info):
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
        mock_add_user_requirement.assert_called_once_with(data["docId"], data["reqNumberId"], data["reqText"], "repo_folder")

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    def test_addRequirement_ServerProblem(self, mock_get_repos_from_file, mock_repo_info):
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqNumberId": "your_req_id",
            "reqText": "your_req_text",
        }
        add_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.post(add_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.addUserRequirement")
    def test_addRequirement_cantBuild(self, mock_add_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_add_user_requirement.return_value = False
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqNumberId": "your_req_id",
            "reqText": "your_req_text",
        }
        add_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.post(add_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.serializeDocReqs")
    @patch("MyServer.restHandlersHelpers.getDocReqs")
    def test_getRequirements(self, mock_get_user_requirement, mock_serialize_doc_reqs, mock_get_repos_from_file, mock_repo_info):
        mock_get_user_requirement.return_value = ["req1", "req2"]
        mock_serialize_doc_reqs.return_value = [{"id": "1", "text": "Req 1", "reviewed": True, "links": ["link1", "link2"]}]
        data = {"docId": "your_doc_id"}
        url = reverse("req") + f'?docId={data["docId"]}'
        response = self.client.get(url)

        mock_get_user_requirement.assert_called_once_with("your_doc_id", "repo_folder")
        mock_serialize_doc_reqs.assert_called_once_with(["req1", "req2"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'[{"id": "1", "text": "Req 1", "reviewed": true, "links": ["link1", "link2"]}]')

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    def test_getRequirements_ServerProblem(self, mock_get_repos_from_file, mock_repo_info):
        url = reverse("req")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    def test_getRequirements_noDocId(self, mock_get_repos_from_file, mock_repo_info):
        url = reverse("req")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("MyServer.repoHelpers.getRepoInfo", return_value=("repo_folder", "repo_name"))
    @patch("MyServer.repoHelpers.getReposFromFile", return_value={"repo_name": "repo_url"})
    @patch("MyServer.restHandlersHelpers.getDocReqs")
    def test_getRequirements_noReqs(self, mock_get_user_requirement, mock_get_repos_from_file, mock_repo_info):
        mock_get_user_requirement.return_value = None
        data = {"docId": "your_doc_id"}
        url = reverse("req") + f'?docId={data["docId"]}'
        response = self.client.get(url)

        mock_get_user_requirement.assert_called_once_with("your_doc_id", "repo_folder")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")
        self.assertEqual(type(response), JsonResponse)
