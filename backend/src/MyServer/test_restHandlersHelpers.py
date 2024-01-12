import unittest
from unittest.mock import patch
import doorstop
import os
import tempfile
import shutil
from MyServer.restHandlersHelpers import (
    addUserDocument,
    addUserLink,
    addUserRequirement,
    buildDicts,
    deleteUserDocument,
    deleteUserRequirement,
    editUserRequirement,
    getAllReqs,
    getDocReqs,
    readServerInfo,
    serializeAllReqs,
    serializeDocReqs,
    serializeDocuments,
)


class TestRestHandlersHelpers(unittest.TestCase):
    def setUp(self):
        # Set up the basic doorstop project structure
        self.test_folder = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_folder, "documents"))
        os.makedirs(os.path.join(self.test_folder, "config"))
        with open(os.path.join(self.test_folder, "config", "settings.yml"), "w") as settings_file:
            settings_file.write("root: documents")

    def tearDown(self):
        # Clean up the test environment
        shutil.rmtree(self.test_folder)

    @staticmethod
    def mock_find_root(cwd):
        return cwd

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

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_add_user_document(self):
        doc_id = "test_doc"
        child_id = "child_doc"
        invalid_req_result = addUserDocument("invalid_doc", "parent", self.test_folder)
        result = addUserDocument(doc_id, None, self.test_folder)
        second_result = addUserDocument(child_id, doc_id, self.test_folder)
        invalid_parent_result_second = addUserDocument("invalid_doc", None, self.test_folder)

        self.assertTrue(result)
        self.assertTrue(second_result)
        self.assertFalse(invalid_req_result)
        self.assertFalse(invalid_parent_result_second)
        self.assertTrue(doc_id in os.listdir(self.test_folder))
        self.assertTrue(child_id in os.listdir(self.test_folder))
        self.assertFalse("invalid_doc" in os.listdir(self.test_folder))

    def test_addUserDocument_not_init(self):
        result = addUserDocument("test_doc", None, "user_folder")
        self.assertFalse(result)

    def test_addUserDocument_throwsError(self):
        with patch("MyServer.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            result = addUserDocument("doc_id", "parent_id", "user_folder")
        self.assertFalse(result)
        with patch("MyServer.restHandlersHelpers.doorstop.build", side_effect=FileNotFoundError("Mocked FileNotFoundError")):
            result = addUserDocument("doc_id", "parent_id", "user_folder")
        self.assertFalse(result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_addUserRequirement(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        result = addUserRequirement(doc_id, 1, "text", self.test_folder)
        self.assertTrue(result)
        self.assertTrue("test_doc001.yml" in os.listdir(self.test_folder + "/" + doc_id))

    @patch("doorstop.build")
    def test_addUserRequirement_typerror(self, mock_buil):
        doc_id = "test_doc"
        mock_build = doorstop.build
        result = addUserDocument(doc_id, None, self.test_folder)
        mock_build.side_effect = TypeError
        result = addUserRequirement(doc_id, 1, "text", self.test_folder)
        self.assertFalse(result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_addUserLink(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        result = addUserLink("test_doc001", "test_doc002", self.test_folder)
        self.assertTrue(result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_delete_user_document(self):
        doc_id = "test_doc"
        child_id = "child_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserDocument(child_id, doc_id, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        addUserLink("test_doc001", "test_doc002", self.test_folder)
        result = deleteUserDocument(doc_id, self.test_folder)
        self.assertTrue(result)
        self.assertTrue(doc_id not in os.listdir(self.test_folder))
        self.assertTrue(child_id not in os.listdir(self.test_folder))
        self.assertFalse(deleteUserDocument("", self.test_folder))

    @patch("doorstop.core.vcs.find_root", side_effect=doorstop.DoorstopError)
    def test_delete_user_document_doorstop_error(self, mock_find_root):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        result = deleteUserDocument(doc_id, self.test_folder)
        self.assertFalse(result)

    @patch("doorstop.core.vcs.find_root", side_effect=FileNotFoundError)
    def test_delete_user_document_file_not_found_error(self, mock_find_root):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        result = deleteUserDocument(doc_id, self.test_folder)
        self.assertFalse(result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    @patch("MyServer.restHandlersHelpers.removeDocTree", return_value=None)
    def test_deleteUserDocument_not_successful(self, mock_build):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        result = deleteUserDocument(doc_id, self.test_folder)
        self.assertFalse(result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_removeUserRequirement(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        addUserLink("test_doc002", "test_doc001", self.test_folder)
        result = deleteUserRequirement("test_doc", "test_doc001", self.test_folder)
        self.assertTrue(result)
        self.assertTrue("test_doc001.yml" not in os.listdir(self.test_folder + "/" + doc_id))

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_editUserRequirement(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        result = editUserRequirement(doc_id, "test_doc001", "new_text", self.test_folder)
        self.assertTrue(result)
        self.assertTrue("new_text" in open(self.test_folder + "/" + doc_id + "/test_doc001.yml").read())

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getDocRequirements(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        result = getDocReqs(doc_id, self.test_folder)
        self.assertTrue(len(result) == 2)
        self.assertTrue("test_doc001" in [str(req.uid) for req in result])

    @patch("doorstop.core.vcs.find_root", side_effect=doorstop.DoorstopError)
    def test_getDocRequirements_doorstop_error(self, mock_find_root):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        result = getDocReqs(doc_id, self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=FileNotFoundError)
    def test_getDocRequirements_file_not_found_error(self, mock_find_root):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        result = getDocReqs(doc_id, self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_buildDicts(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserDocument("test_child_1", doc_id, self.test_folder)
        tree = doorstop.build(self.test_folder)
        result = buildDicts(tree)
        expected_result = {"prefix": doc_id, "children": [{"prefix": "test_child_1", "children": []}]}
        self.assertEqual(result, expected_result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeDocuments(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserDocument("test_child_1", doc_id, self.test_folder)
        addUserDocument("test_child_2", doc_id, self.test_folder)

        result = serializeDocuments(self.test_folder)
        expected_result = [{"prefix": "test_doc", "children": [{"prefix": "test_child_2", "children": []}, {"prefix": "test_child_1", "children": []}]}]
        self.assertEqual(result[0]["prefix"], expected_result[0]["prefix"])
        self.assertTrue(len(result[0]["children"]) == len(expected_result[0]["children"]))
        self.assertTrue(result[0]["children"][0]["prefix"] in [child["prefix"] for child in expected_result[0]["children"]])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeDocuments_no_documents(self):
        result = serializeDocuments(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=doorstop.DoorstopError)
    def test_serializeDocuments_doorstop_error(self, mock_find_root):
        result = serializeDocuments(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=FileNotFoundError)
    def test_serializeDocuments_file_not_found_error(self, mock_find_root):
        result = serializeDocuments(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeDocReqs(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        addUserLink("test_doc001", "test_doc002", self.test_folder)
        reqs = getDocReqs(doc_id, self.test_folder)
        result = serializeDocReqs(reqs)
        expected_result = [
            {"id": "test_doc001", "text": "text", "reviewed": False, "links": ["test_doc002"]},
            {"id": "test_doc002", "text": "text", "reviewed": False, "links": []},
        ]
        self.assertEqual(len(result), len(expected_result))
        self.assertTrue(result[0]["id"] in [req["id"] for req in expected_result])
        self.assertTrue(result[0]["text"] in [req["text"] for req in expected_result])
        self.assertTrue(expected_result[0]["reviewed"] in [req["reviewed"] for req in result])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getAllReqs(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserDocument("test_child_1", doc_id, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        result = getAllReqs(self.test_folder)
        self.assertEqual(result[0][1], "test_doc")
        self.assertEqual(len(result), 2)
        self.assertTrue("test_doc001" in [str(req[0].uid) for req in result])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getAllReqs_no_documents(self):
        result = getAllReqs(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=doorstop.DoorstopError)
    def test_getAllReqs_doorstop_error(self, mock_find_root):
        result = getAllReqs(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=FileNotFoundError)
    def test_getAllReqs_file_not_found_error(self, mock_find_root):
        result = getAllReqs(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeAllReqs(self):
        doc_id = "test_doc"
        addUserDocument(doc_id, None, self.test_folder)
        addUserRequirement(doc_id, 1, "text", self.test_folder)
        addUserRequirement(doc_id, 2, "text", self.test_folder)
        addUserLink("test_doc001", "test_doc002", self.test_folder)
        reqs = getAllReqs(self.test_folder)
        result = serializeAllReqs(reqs)
        expected_result = [
            {"id": "test_doc001", "text": "text", "reviewed": False, "links": ["test_doc002"], "docPrefix": doc_id},
            {"id": "test_doc002", "text": "text", "reviewed": False, "links": [], "docPrefix": doc_id},
        ]
        self.assertEqual(len(result), len(expected_result))
        self.assertTrue(result[0]["id"] in [req["id"] for req in expected_result])
        self.assertTrue(expected_result[0]["links"] in [req["links"] for req in result])
        self.assertTrue(result[0]["text"] in [req["text"] for req in expected_result])


if __name__ == "__main__":
    unittest.main()
