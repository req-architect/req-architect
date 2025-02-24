import unittest
from unittest.mock import patch
import doorstop
import os
import tempfile
import shutil
import api.error as my_errors

import yaml
from api.restHandlersHelpers import (
    add_user_document,
    add_user_link,
    add_user_requirement,
    build_dicts,
    delete_user_document,
    delete_user_link,
    delete_user_requirement,
    edit_user_requirement,
    get_all_reqs,
    get_doc_reqs,
    serialize_all_reqs,
    serialize_doc_reqs,
    serialize_documents,
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

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_add_user_document(self):
        doc_id = "test_doc"
        child_id = "child_doc"
        self.assertRaises(my_errors.ParentOfEmptyTreeSpecifiedException, add_user_document, "invalid_doc", "parent", self.test_folder)
        add_user_document(doc_id, None, self.test_folder)
        add_user_document(child_id, doc_id, self.test_folder)
        self.assertRaises(my_errors.NoParentSpecifiedException, add_user_document, "invalid_doc", None, self.test_folder)

        self.assertTrue(doc_id in os.listdir(self.test_folder))
        self.assertTrue(child_id in os.listdir(self.test_folder))
        self.assertFalse("invalid_doc" in os.listdir(self.test_folder))

    def test_addUserDocument_not_init(self):
        self.assertRaises(my_errors.DoorstopException, add_user_document, "test_doc", None, "user_folder")

    def test_addUserDocument_throwsError(self):
        self.assertRaises(my_errors.DoorstopException, add_user_document, "doc_id", "parent_id", "user_folder")
        with patch("api.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            self.assertRaises(my_errors.DoorstopException, add_user_document, "doc_id", "parent_id", "user_folder")

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_addUserRequirement(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        self.assertTrue("test_doc001.yml" in os.listdir(self.test_folder + "/" + doc_id))

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_addUserRequirement_throws(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        self.assertRaises(my_errors.DocNotFoundException, add_user_requirement, "a", 1, "text", self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        self.assertRaises(my_errors.InvalidReqIDException, add_user_requirement, doc_id, 1, "text", self.test_folder)
        with patch("api.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            self.assertRaises(my_errors.DoorstopException, add_user_requirement, doc_id, 2, "text", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_addUserLink(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc001", "test_doc002", self.test_folder)
        self.assertTrue("test_doc001.yml" in os.listdir(self.test_folder + "/" + doc_id))
        self.assertTrue("test_doc002.yml" in os.listdir(self.test_folder + "/" + doc_id))
        file_path = os.path.join(self.test_folder, doc_id, "test_doc001.yml")
        with open(file_path, "r") as file:
            content = yaml.safe_load(file)
        links = content.get("links", [])
        keys = [link.keys() for link in links]
        self.assertTrue(any('test_doc002' in key for key in keys))

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_addUserLink_throws(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        self.assertRaises(my_errors.LinkCycleException, add_user_link, "test_doc001", "invalid_req", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_deleteUserLink_invalid_req(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc001", "test_doc002", self.test_folder)
        self.assertRaises(my_errors.ReqNotFoundException, delete_user_link, "test_doc001", "invalid_req", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_delete_user_document(self):
        doc_id = "test_doc"
        child_id = "child_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_document(child_id, doc_id, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc001", "test_doc002", self.test_folder)
        delete_user_document(doc_id, self.test_folder)
        self.assertTrue(doc_id not in os.listdir(self.test_folder))
        self.assertTrue(child_id not in os.listdir(self.test_folder))
        self.assertRaises(my_errors.EmptyDocumentTreeException, delete_user_document, "invalid_doc", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_delete_user_document_doorstop_error(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        with patch("api.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            self.assertRaises(my_errors.DoorstopException, delete_user_document, doc_id, self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_delete_user_document_non_existend_doc(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        self.assertRaises(my_errors.DocNotFoundException, delete_user_document, "nonexistent_doc_id", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_delete_user_document_no_docs(self):
        self.assertRaises(my_errors.EmptyDocumentTreeException, delete_user_document, "invalid_doc", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_removeUserRequirement(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc002", "test_doc001", self.test_folder)
        delete_user_requirement("test_doc", "test_doc001", self.test_folder)
        self.assertTrue("test_doc001.yml" not in os.listdir(self.test_folder + "/" + doc_id))

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_removeUserRequirement_throws(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc002", "test_doc001", self.test_folder)
        with patch("api.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            self.assertRaises(my_errors.DoorstopException, delete_user_requirement, "test_doc", "test_doc001", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_editUserRequirement(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        edit_user_requirement(doc_id, "test_doc001", "new_text", self.test_folder)
        self.assertTrue("new_text" in open(self.test_folder + "/" + doc_id + "/test_doc001.yml").read())

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_editUserRequirement_throws(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        self.assertRaises(my_errors.DoorstopException, edit_user_requirement, "invalid", "test_doc001", "new_text", self.test_folder)
        self.assertRaises(my_errors.ReqNotFoundException, edit_user_requirement, doc_id, "test_doc011", "new_text", self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getDocRequirements(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        result = get_doc_reqs(doc_id, self.test_folder)
        self.assertTrue(len(result) == 2)
        self.assertTrue("test_doc001" in [str(req.uid) for req in result])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getDocRequirements_doorstop_error(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        with patch("api.restHandlersHelpers.doorstop.build", side_effect=doorstop.DoorstopError("Mocked DoorstopError")):
            self.assertRaises(my_errors.DoorstopException, get_doc_reqs, doc_id, self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getDocRequirements_not_found_error(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        with patch("api.restHandlersHelpers.doorstop.build", side_effect=FileNotFoundError("Mocked FileNotFoundError")):
            self.assertRaises(my_errors.DocNotFoundException, get_doc_reqs, doc_id, self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_buildDicts(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_document("test_child_1", doc_id, self.test_folder)
        tree = doorstop.build(self.test_folder)
        result = build_dicts(tree)
        expected_result = {"prefix": doc_id, "children": [{"prefix": "test_child_1", "children": []}]}
        self.assertEqual(result, expected_result)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeDocuments(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_document("test_child_1", doc_id, self.test_folder)
        add_user_document("test_child_2", doc_id, self.test_folder)

        result = serialize_documents(self.test_folder)
        expected_result = [{"prefix": "test_doc", "children": [{"prefix": "test_child_2", "children": []}, {"prefix": "test_child_1", "children": []}]}]
        self.assertEqual(result[0]["prefix"], expected_result[0]["prefix"])
        self.assertTrue(len(result[0]["children"]) == len(expected_result[0]["children"]))
        self.assertTrue(result[0]["children"][0]["prefix"] in [child["prefix"] for child in expected_result[0]["children"]])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeDocuments_no_documents(self):
        result = serialize_documents(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=doorstop.DoorstopError)
    def test_serializeDocuments_doorstop_error(self, mock_find_root):
        self.assertRaises(my_errors.DoorstopException, serialize_documents, self.test_folder)

    @patch("doorstop.core.vcs.find_root", side_effect=FileNotFoundError)
    def test_serializeDocuments_file_not_found_error(self, mock_find_root):
        self.assertRaises(FileNotFoundError, serialize_documents, self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeDocReqs(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc001", "test_doc002", self.test_folder)
        reqs = get_doc_reqs(doc_id, self.test_folder)
        result = serialize_doc_reqs(reqs)
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
        add_user_document(doc_id, None, self.test_folder)
        add_user_document("test_child_1", doc_id, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        result = get_all_reqs(self.test_folder)
        self.assertEqual(result[0][1], "test_doc")
        self.assertEqual(len(result), 2)
        self.assertTrue("test_doc001" in [str(req[0].uid) for req in result])

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_getAllReqs_no_documents(self):
        result = get_all_reqs(self.test_folder)
        self.assertEqual(result, [])

    @patch("doorstop.core.vcs.find_root", side_effect=doorstop.DoorstopError)
    def test_getAllReqs_doorstop_error(self, mock_find_root):
        self.assertRaises(my_errors.DoorstopException, get_all_reqs, self.test_folder)

    @patch("doorstop.core.vcs.find_root", side_effect=FileNotFoundError)
    def test_getAllReqs_file_not_found_error(self, mock_find_root):
        self.assertRaises(FileNotFoundError, get_all_reqs, self.test_folder)

    @patch("doorstop.core.vcs.find_root", new=mock_find_root)
    def test_serializeAllReqs(self):
        doc_id = "test_doc"
        add_user_document(doc_id, None, self.test_folder)
        add_user_requirement(doc_id, 1, "text", self.test_folder)
        add_user_requirement(doc_id, 2, "text", self.test_folder)
        add_user_link("test_doc001", "test_doc002", self.test_folder)
        reqs = get_all_reqs(self.test_folder)
        result = serialize_all_reqs(reqs)
        expected_result = [
            {"id": "test_doc001", "text": "text", "reviewed": False, "links": ["test_doc002"], "docPrefix": doc_id},
            {"id": "test_doc002", "text": "text", "reviewed": False, "links": [], "docPrefix": doc_id},
        ]
        self.assertEqual(len(result), len(expected_result))
        self.assertTrue(result[0]["id"] in [req["id"] for req in expected_result])
        self.assertTrue(expected_result[0]["links"] in [req["links"] for req in result])
        self.assertTrue(result[0]["text"] in [req["text"] for req in expected_result])
