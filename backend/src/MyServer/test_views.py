from django.http import JsonResponse
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import MagicMock, patch
import json


class TestViews(SimpleTestCase):
    @patch("MyServer.restHandlersHelpers.deleteUserRequirement")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_deleteRequirement(self, mock_read_server_info, mock_delete_user_requirement):
        mock_delete_user_requirement.return_value = True
        mock_read_server_info.return_value = {"usersFolder": "app"}
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete.data["message"], "OK")
        mock_delete_user_requirement.assert_called_once_with(data["docId"], data["reqId"], "app/user")

    def test_deleteRequirement_ServerProblem(self):
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.deleteUserRequirement")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_deleteRequirement_cantBuild(self, mock_read_server_info, mock_delete_user_requirement):
        mock_delete_user_requirement.return_value = False
        mock_read_server_info.return_value = {"usersFolder": "app"}
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
        }
        delete_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.delete(delete_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.editUserRequirement")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_editRequirement(self, mock_read_server_info, mock_edit_user_requirement):
        mock_edit_user_requirement.return_value = True
        mock_read_server_info.return_value = {"usersFolder": "app"}
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
        mock_edit_user_requirement.assert_called_once_with(data["docId"], data["reqId"], data["reqText"], "app/user")

    def test_editRequirement_ServerProblem(self):
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
            "reqText": "your_req_text",
        }
        edit_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.put(edit_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.editUserRequirement")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_editRequirement_canBuild(self, mock_read_server_info, mock_edit_user_requirement):
        mock_edit_user_requirement.return_value = False
        mock_read_server_info.return_value = {"usersFolder": "app"}
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqId": "your_req_id",
            "reqText": "your_req_text",
        }

        edit_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.put(edit_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.addUserRequirement")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_addRequirement(self, mock_read_server_info, mock_add_user_requirement):
        mock_add_user_requirement.return_value = True
        mock_read_server_info.return_value = {"usersFolder": "app"}
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
        mock_add_user_requirement.assert_called_once_with(data["docId"], data["reqNumberId"], data["reqText"], "app/user")

    def test_addRequirement_ServerProblem(self):
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqNumberId": "your_req_id",
            "reqText": "your_req_text",
        }
        add_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.post(add_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.addUserRequirement")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_addRequirement_cantBuild(self, mock_read_server_info, mock_add_user_requirement):
        mock_add_user_requirement.return_value = False
        mock_read_server_info.return_value = {"usersFolder": "app"}
        url = reverse("req")
        data = {
            "docId": "your_doc_id",
            "reqNumberId": "your_req_id",
            "reqText": "your_req_text",
        }
        add_url = f"{url}?docId={data['docId']}"
        response_delete = self.client.post(add_url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response_delete.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.serializeDocReqs")
    @patch("MyServer.restHandlersHelpers.getDocReqs")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_getRequirements(self, mock_read_server_info, mock_get_user_requirement, mock_serialize_doc_reqs):
        mock_get_user_requirement.return_value = ["req1", "req2"]
        mock_read_server_info.return_value = {"usersFolder": "app"}
        mock_serialize_doc_reqs.return_value = [{"id": "1", "text": "Req 1", "reviewed": True, "links": ["link1", "link2"]}]
        data = {"docId": "your_doc_id"}
        url = reverse("req") + f'?docId={data["docId"]}'
        response = self.client.get(url)

        mock_get_user_requirement.assert_called_once_with("your_doc_id", "app/user")
        mock_serialize_doc_reqs.assert_called_once_with(["req1", "req2"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'[{"id": "1", "text": "Req 1", "reviewed": true, "links": ["link1", "link2"]}]')

    def test_getRequirements_ServerProblem(self):
        url = reverse("req")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_getRequirements_noDocId(self, mock_read_server_info):
        mock_read_server_info.return_value = {"usersFolder": "app"}
        url = reverse("req")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("MyServer.restHandlersHelpers.getDocReqs")
    @patch("MyServer.restHandlersHelpers.readServerInfo")
    def test_getRequirements_noReqs(self, mock_read_server_info, mock_get_user_requirement):
        mock_get_user_requirement.return_value = None
        mock_read_server_info.return_value = {"usersFolder": "app"}
        data = {"docId": "your_doc_id"}
        url = reverse("req") + f'?docId={data["docId"]}'
        response = self.client.get(url)

        mock_get_user_requirement.assert_called_once_with("your_doc_id", "app/user")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")
        self.assertEqual(type(response), JsonResponse)
