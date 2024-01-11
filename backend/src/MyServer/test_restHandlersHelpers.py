import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
import doorstop
import os
import tempfile
import shutil
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

    @patch("MyServer.restHandlersHelpers.checkIfExists", return_value=False)
    @patch("MyServer.restHandlersHelpers.initRepoFolder", return_value=False)
    def test_addUserDocument_not_init(self, mock_initRepoFolder, mock_checkIfExists):
        result = addUserDocument("test_doc", None, "user_folder")
        self.assertFalse(result)
        mock_checkIfExists.assert_called_once_with("user_folder")
        mock_initRepoFolder.assert_called_once_with("user_folder")

    @patch("MyServer.restHandlersHelpers.checkIfExists", return_value=True)
    def test_addUserDocument_throwsError(self, mock_check_exists):
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


if __name__ == "__main__":
    unittest.main()
