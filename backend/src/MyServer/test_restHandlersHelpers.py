import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
import doorstop
from MyServer.restHandlersHelpers import (
    RemoveLinksToReq,
    addUserDocument,
    addUserLink,
    addUserRequirement,
    buildDicts,
    checkIfExists,
    deleteUserDocument,
    deleteUserLink,
    deleteUserRequirement,
    editUserRequirement,
    getDocReqs,
    initRepoFolder,
    readServerInfo,
    removeDocTree,
)


class TestRestHandlersHelpers(unittest.TestCase):
    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="HOST 127.0.0.1\nPORT 8080")
    def test_readServerInfo(self, mock_open):
        result = readServerInfo("sample_server_info.txt")

        expected_result = {"HOST": "127.0.0.1", "PORT": "8080"}
        self.assertEqual(result, expected_result)

        mock_open.assert_called_once_with("sample_server_info.txt", "r")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_readServerInfo_FileNotFound(self, mock_open):
        result = readServerInfo("sample_server_info.txt")

        self.assertIsNone(result)

        mock_open.assert_called_once_with("sample_server_info.txt", "r")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="INVALID_DATA")
    def test_readServerInfo_index_error(self, mock_open):
        result = readServerInfo("sample_server_info.txt")

        self.assertIsNone(result)

        mock_open.assert_called_once_with("sample_server_info.txt", "r")

    @patch("os.path.exists", return_value=True)
    def test_checkIfExists_folder_exists(self, mock_exists):
        result = checkIfExists("existing_folder")

        self.assertTrue(result)

        mock_exists.assert_called_once_with("existing_folder")

    @patch("os.path.exists", return_value=False)
    def test_checkIfExists_folder_not_exists(self, mock_exists):
        result = checkIfExists("nonexistent_folder")

        self.assertFalse(result)

        mock_exists.assert_called_once_with("nonexistent_folder")

    @patch("MyServer.restHandlersHelpers.git.Repo")
    @patch("os.makedirs")
    def test_initRepoFolder(self, mock_makedirs, mock_repo):
        result = initRepoFolder("user_folder")

        mock_makedirs.assert_called_once_with("user_folder")

        mock_repo.init.assert_called_once_with(path="user_folder")

        self.assertIsInstance(result, MagicMock)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    @patch("MyServer.restHandlersHelpers.checkIfExists")
    @patch("MyServer.restHandlersHelpers.initRepoFolder")
    def test_addUserDocument(self, mock_init_repo, mock_check_exists, mock_build):
        mock_check_exists.return_value = True
        mock_init_repo.return_value = MagicMock()
        mock_doc_tree = MagicMock()
        mock_doc_tree.documents = ["doc1"]
        mock_build.return_value = mock_doc_tree

        result = addUserDocument("doc_id", "parent_id", "user_folder")

        mock_check_exists.assert_called_once_with("user_folder")
        mock_build.assert_called_once_with(cwd="user_folder")
        self.assertTrue(result)

    @patch("MyServer.restHandlersHelpers.checkIfExists")
    @patch("MyServer.restHandlersHelpers.initRepoFolder")
    def test_addUserDocument_not_init(self, mock_init_repo, mock_check_exists):
        mock_check_exists.return_value = False
        mock_init_repo.return_value = False

        result = addUserDocument("doc_id", "parent_id", "user_folder")

        mock_check_exists.assert_called_once_with("user_folder")
        mock_init_repo.assert_called_once_with("user_folder")
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    @patch("MyServer.restHandlersHelpers.checkIfExists")
    @patch("MyServer.restHandlersHelpers.initRepoFolder")
    def test_addUserDocument_zero_doc_and_parent(self, mock_init_repo, mock_check_exists, mock_build):
        mock_check_exists.return_value = True
        mock_init_repo.return_value = MagicMock()
        mock_doc_tree = MagicMock()
        mock_doc_tree.documents = []
        mock_build.return_value = mock_doc_tree

        result = addUserDocument("doc_id", "parent_id", "user_folder")

        mock_check_exists.assert_called_once_with("user_folder")
        mock_build.assert_called_once_with(cwd="user_folder")
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    @patch("MyServer.restHandlersHelpers.checkIfExists")
    @patch("MyServer.restHandlersHelpers.initRepoFolder")
    def test_addUserDocument_one_doc_and_no_parent(self, mock_init_repo, mock_check_exists, mock_build):
        mock_check_exists.return_value = True
        mock_init_repo.return_value = MagicMock()
        mock_doc_tree = MagicMock()
        mock_doc_tree.documents = ["doc1"]
        mock_build.return_value = mock_doc_tree

        result = addUserDocument("doc_id", None, "user_folder")

        mock_check_exists.assert_called_once_with("user_folder")
        mock_build.assert_called_once_with(cwd="user_folder")
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    @patch("MyServer.restHandlersHelpers.checkIfExists")
    @patch("MyServer.restHandlersHelpers.initRepoFolder")
    def test_addUserDocument_DoorstopError(self, mock_init_repo, mock_check_exists, mock_build):
        mock_check_exists.return_value = True
        mock_init_repo.return_value = MagicMock()
        mock_doc_tree = MagicMock()
        mock_doc_tree.documents = ["doc1"]
        mock_build.return_value = mock_doc_tree

        with patch("MyServer.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            result = addUserDocument("doc_id", "parent_id", "user_folder")

        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    @patch("MyServer.restHandlersHelpers.checkIfExists")
    @patch("MyServer.restHandlersHelpers.initRepoFolder")
    def test_addUserDocument_File_notFound_error(self, mock_init_repo, mock_check_exists, mock_build):
        mock_check_exists.return_value = True
        mock_init_repo.return_value = MagicMock()
        mock_doc_tree = MagicMock()
        mock_doc_tree.documents = ["doc1"]
        mock_build.return_value = mock_doc_tree

        with patch("MyServer.restHandlersHelpers.doorstop.build", side_effect=FileNotFoundError("Mocked FileNotFoundError")):
            result = addUserDocument("doc_id", "parent_id", "user_folder")

        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.rmtree")
    @patch("MyServer.restHandlersHelpers.RemoveLinksToReq")
    def test_removeDocTree(self, mock_remove_links, mock_rmtree):
        mock_req1 = MagicMock()
        mock_req1.uid = "mocked_req_uid"
        mock_doc1 = MagicMock()
        mock_doc1.prefix = "doc1"
        mock_doc1_path = "path/to/doc1"
        mock_doc1.path = mock_doc1_path
        mock_doc1.items = [mock_req1]

        mock_doc2 = MagicMock()
        mock_doc2.prefix = "doc2"
        mock_doc2_path = "path/to/doc2"
        mock_doc2.path = mock_doc2_path

        mock_tree = MagicMock()
        mock_tree.document = mock_doc1
        mock_tree.documents = [mock_doc1, mock_doc2]

        mock_root_tree = MagicMock()
        mock_root_tree.documents = [mock_doc1, mock_doc2]

        removeDocTree(mock_tree, "doc1", "user_folder", mock_root_tree)

        mock_remove_links.assert_called_once_with("mocked_req_uid", [], "user_folder")

        mock_rmtree.assert_any_call(mock_doc1_path)
        mock_rmtree.assert_any_call(mock_doc2_path)

        self.assertEqual(mock_rmtree.call_count, len(mock_tree.documents))

    @patch("MyServer.restHandlersHelpers.removeDocTree")
    def test_removeDocTree_recursive(self, mock_removeDocTree):
        mock_tree = MagicMock()
        mock_child_tree = MagicMock()
        mock_tree.children = [mock_child_tree]

        removeDocTree(mock_tree, "doc1", "user_folder", mock_tree)

        mock_removeDocTree.assert_called_once_with(mock_child_tree, "doc1", "user_folder", mock_tree)

    @patch("MyServer.restHandlersHelpers.removeDocTree")
    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_deleteUserDocument(self, mock_build, mock_removeDocTree):
        mock_document1 = MagicMock()
        mock_document2 = MagicMock()
        mock_tree1 = MagicMock()
        mock_tree1.documents = [mock_document1, mock_document2]
        mock_tree2 = MagicMock()
        mock_tree2.documents = []
        mock_build.side_effect = [mock_tree1, mock_tree2]

        result = deleteUserDocument("doc1", "user_folder")
        mock_build.assert_has_calls([mock.call("user_folder"), mock.call("user_folder")])
        mock_removeDocTree.assert_called_once_with(mock_tree1, "doc1", "user_folder", mock_tree1)
        self.assertTrue(result)

    @patch("MyServer.restHandlersHelpers.removeDocTree")
    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_deleteUserDocumentNotDeleted(self, mock_build, mock_removeDocTree):
        mock_document1 = MagicMock()
        mock_document2 = MagicMock()
        mock_tree1 = MagicMock()
        mock_tree1.documents = [mock_document1, mock_document2]
        mock_tree2 = MagicMock()
        mock_tree2.documents = [mock_document1, mock_document2]
        mock_build.side_effect = [mock_tree1, mock_tree2]

        result = deleteUserDocument("doc1", "user_folder")
        mock_build.assert_has_calls([mock.call("user_folder"), mock.call("user_folder")])
        mock_removeDocTree.assert_called_once_with(mock_tree1, "doc1", "user_folder", mock_tree1)
        self.assertFalse(result)

    def test_deleteUserDocumentFileNotFoundError(self):
        with patch("MyServer.restHandlersHelpers.doorstop.build", side_effect=FileNotFoundError("Mocked FileNotFoundError")):
            result = deleteUserDocument("doc1", "user_folder")
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_deleteUserDocumentNoDocuments(self, mock_build):
        mock_tree1 = MagicMock()
        mock_tree1.documents = []
        mock_build.side_effect = [mock_tree1]

        result = deleteUserDocument("doc1", "user_folder")
        mock_build.assert_has_calls([mock.call("user_folder")])
        self.assertFalse(result)

    def test_deleteUserDocumentDoorstopError(self):
        with patch("MyServer.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            result = deleteUserDocument("doc1", "user_folder")
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_add_user_requirement_success(self, mock_build):
        mock_doc = mock_build.return_value
        mock_add_item = mock_doc.find_document.return_value.add_item
        doc_id = "test_doc"
        req_number_id = 1
        req_text = "Test Requirement"
        user_folder = "/path/to/user"
        result = addUserRequirement(doc_id, req_number_id, req_text, user_folder)

        mock_build.assert_called_once_with(user_folder)
        mock_doc.find_document.assert_called_once_with(doc_id)
        mock_add_item.assert_called_once_with(number=req_number_id)
        self.assertTrue(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_add_user_requirement_DoorstopError(self, mock_build):
        mock_build.side_effect = doorstop.DoorstopError("Test DoorstopError")
        doc_id = "test_doc"
        req_number_id = 1
        req_text = "Test Requirement"
        user_folder = "/path/to/user"
        result = addUserRequirement(doc_id, req_number_id, req_text, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_add_user_requirement_TypeError(self, mock_build):
        mock_build.side_effect = TypeError("Test TypeError")
        doc_id = "test_doc"
        req_number_id = 1
        req_text = "Test Requirement"
        user_folder = "/path/to/user"
        result = addUserRequirement(doc_id, req_number_id, req_text, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_add_user_requirement_FileNotFoundError(self, mock_build):
        mock_build.side_effect = FileNotFoundError("Test FileNotFoundError")
        doc_id = "test_doc"
        req_number_id = 1
        req_text = "Test Requirement"
        user_folder = "/path/to/user"
        result = addUserRequirement(doc_id, req_number_id, req_text, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.deleteUserLink")
    def test_remove_links_to_req(self, mock_delete_user_link):
        mock_delete_user_link.return_value = True
        req_id = "test_req_id"
        user_folder = "/path/to/user"
        mock_document1 = MagicMock()
        mock_document2 = MagicMock()
        mock_documents = [mock_document1, mock_document2]
        mock_req1 = MagicMock(uid="1")
        mock_req2 = MagicMock(uid="2")
        mock_req3 = MagicMock(uid="3")
        mock_document1.items = [mock_req1, mock_req2]
        mock_document2.items = [mock_req3]
        RemoveLinksToReq(req_id, mock_documents, user_folder)
        expected_calls = [
            unittest.mock.call(str(mock_req1.uid), req_id, user_folder),
            unittest.mock.call(str(mock_req2.uid), req_id, user_folder),
            unittest.mock.call(str(mock_req3.uid), req_id, user_folder),
        ]
        mock_delete_user_link.assert_has_calls(expected_calls, any_order=True)

    @patch("MyServer.restHandlersHelpers.RemoveLinksToReq")
    def test_delete_user_requirement_success(self, mock_remove_links):
        mock_remove_links.return_value = True
        doc_id = "test_doc"
        req_uid = "test_req_uid"
        user_folder = "/path/to/user"
        mock_doc = MagicMock()
        mock_build = MagicMock(return_value=mock_doc)
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = deleteUserRequirement(doc_id, req_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_doc.find_document.assert_called_once_with(doc_id)
        mock_remove_links.assert_called_once_with(req_uid, mock_doc.documents, user_folder)
        self.assertTrue(result)

    @patch("MyServer.restHandlersHelpers.RemoveLinksToReq")
    def test_delete_user_requirement_doorstop_error(self, mock_remove_links):
        mock_remove_links.return_value = True
        doc_id = "test_doc"
        req_uid = "test_req_uid"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=doorstop.DoorstopError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = deleteUserRequirement(doc_id, req_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_remove_links.assert_not_called()
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.RemoveLinksToReq")
    def test_delete_user_requirement_file_not_found_error(self, mock_remove_links):
        mock_remove_links.return_value = True
        doc_id = "test_doc"
        req_uid = "test_req_uid"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=FileNotFoundError("Test FileNotFoundError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = deleteUserRequirement(doc_id, req_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_remove_links.assert_not_called()
        self.assertFalse(result)

    def test_edit_user_requirement_success(self):
        doc_id = "test_doc"
        req_uid = "test_req_uid"
        req_text = "new_req_text"
        user_folder = "/path/to/user"
        mock_doc = MagicMock()
        mock_build = MagicMock(return_value=mock_doc)
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = editUserRequirement(doc_id, req_uid, req_text, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_doc.find_document.assert_called_once_with(doc_id)
        self.assertTrue(result)

    def test_edit_user_requirement_DoorstopError(self):
        doc_id = "test_doc"
        req_uid = "test_req_uid"
        req_text = "new_req_text"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=doorstop.DoorstopError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = editUserRequirement(doc_id, req_uid, req_text, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    def test_add_user_link_success(self):
        req1_uid = "req1_uid"
        req2_uid = "req2_uid"
        user_folder = "/path/to/user"
        mock_doc_tree = MagicMock()
        mock_build = MagicMock(return_value=mock_doc_tree)
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = addUserLink(req1_uid, req2_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_doc_tree.link_items.assert_called_once_with(req1_uid, req2_uid)
        self.assertTrue(result)

    def test_add_user_link_DoorstopError(self):
        req1_uid = "req1_uid"
        req2_uid = "req2_uid"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=doorstop.DoorstopError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = addUserLink(req1_uid, req2_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    def test_add_user_link_FileNotFound(self):
        req1_uid = "req1_uid"
        req2_uid = "req2_uid"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=FileNotFoundError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = addUserLink(req1_uid, req2_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    def test_delete_user_link_success(self):
        req1_uid = "req1_uid"
        req2_uid = "req2_uid"
        user_folder = "/path/to/user"
        mock_doc_tree = MagicMock()
        mock_build = MagicMock(return_value=mock_doc_tree)
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = deleteUserLink(req1_uid, req2_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_doc_tree.unlink_items.assert_called_once_with(req1_uid, req2_uid)
        self.assertTrue(result)

    def test_delete_user_link_DoorstopError(self):
        req1_uid = "req1_uid"
        req2_uid = "req2_uid"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=doorstop.DoorstopError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = deleteUserLink(req1_uid, req2_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    def test_delete_user_link_FileNotFoundError(self):
        req1_uid = "req1_uid"
        req2_uid = "req2_uid"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=FileNotFoundError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = deleteUserLink(req1_uid, req2_uid, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertFalse(result)

    @patch("MyServer.restHandlersHelpers.doorstop.build")
    def test_get_doc_reqs_success(self, mock_build):
        doc_id = "your_doc_id"
        user_folder = "/path/to/user"
        mock_item1 = Mock(uid="req1")
        mock_item2 = Mock(uid="req2")
        mock_build.return_value = Mock()
        mock_build.return_value.find_document = Mock()
        mock_build.return_value.find_document.return_value.items = [mock_item1, mock_item2]
        result = getDocReqs(doc_id, user_folder)
        mock_build.assert_called_once_with(user_folder)
        mock_build.return_value.find_document.assert_called_once_with(doc_id)
        self.assertEqual(result[0].uid, "req1")
        self.assertEqual(result[1].uid, "req2")

    def test_get_doc_reqs_DoorstopError(self):
        doc_id = "your_doc_id"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=doorstop.DoorstopError("Test DoorstopError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = getDocReqs(doc_id, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertEqual(result, [])

    def test_get_doc_reqs_FileNotFoundError(self):
        doc_id = "your_doc_id"
        user_folder = "/path/to/user"
        mock_build = MagicMock(side_effect=FileNotFoundError("Test FileNotFoundError"))
        with patch("MyServer.restHandlersHelpers.doorstop.build", mock_build):
            result = getDocReqs(doc_id, user_folder)
        mock_build.assert_called_once_with(user_folder)
        self.assertEqual(result, [])

    def test_build_dicts_with_children(self):
        mock_document = MagicMock(prefix="mock_prefix")
        mock_child = MagicMock(prefix="mock_child_prefix")
        mock_tree_instance = MagicMock()
        mock_tree_instance.document = mock_document
        mock_tree_instance.children = [mock_child]
        result = buildDicts(mock_tree_instance)
        expected_result = {"prefix": "mock_prefix", "children": [{"prefix": "mock_child_prefix", "children": []}]}
        self.assertEqual(result["prefix"], expected_result["prefix"])
        self.assertEqual(result["children"][0]["children"], expected_result["children"][0]["children"])


if __name__ == "__main__":
    unittest.main()
