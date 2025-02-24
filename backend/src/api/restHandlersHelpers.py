from shutil import rmtree
import api.error
import doorstop

"""
Module to handle communication with the Doorstop API for modifying, adding and deleting requirements and project documents.

It contains functions for adding and removing documents and requirements and for modifying requirements, as well as functions for wrapping the logic for preparing
representation of existing documents and requirements to customers.
"""


def add_user_document(doc_id: str, parent_id: str, user_folder: str):
    """
    Function containing the logic for adding a document. It uses the document tree from the Doorstop API to manage the process of adding a new document by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client via the
    appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(cwd=user_folder)
        if len(doc_tree.documents) >= 1 and not parent_id:
            raise api.error.NoParentSpecifiedException(f"parentID must be specified for the given document.")
        if len(doc_tree.documents) == 0 and parent_id:
            raise api.error.ParentOfEmptyTreeSpecifiedException()
        doc_name = user_folder + "/" + doc_id
        doc_tree.create_document(
            doc_name, doc_id, parent=parent_id)
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build document tree.")
    except FileNotFoundError:
        raise api.error.DoorstopException(f"User folder {user_folder} was not found.")


def remove_doc_tree(tree: doorstop.Tree, doc_id: str, user_folder: str, root_tree: doorstop.Tree):
    """
    Function containing the logic for removing a specific subtree from the project document tree. It uses the tree from the Doorstop API to manage the process of deleting an existing subtree by calling the
    appropriate Doorstop functions.
    """
    doc = tree.document
    if doc.prefix == doc_id:
        to_be_removed = tree.documents
        to_check = [
            document for document in root_tree.documents if document not in to_be_removed]
        for document in to_be_removed:
            for req in document.items:
                remove_links_to_req(str(req.uid), to_check, user_folder)
        for document in tree.documents:
            rmtree(document.path)
        return
    for child in tree.children:
        remove_doc_tree(child, doc_id, user_folder, root_tree)
    return


def delete_user_document(doc_id: str, user_folder: str):
    """
    Function containing the logic for deleting a document. Uses the document tree from the Doorstop API to manage the process of deleting an existing document by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        number_of_documents = len(doc_tree.documents)
        if number_of_documents == 0:
            raise api.error.EmptyDocumentTreeException(f"No documents were created yet.")
        try:
            doc_tree.find_document(doc_id)
        except doorstop.DoorstopError:
            raise api.error.DocNotFoundException(f"Document of given UID: {doc_id} was not found.")
        remove_doc_tree(doc_tree, doc_id, user_folder, doc_tree)
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build document tree.")


def add_user_requirement(doc_id: str, req_number_id: int, req_text: str, user_folder: str):
    """
    Function containing the logic for adding a requirement. It uses the document tree from the Doorstop API to manage the process of adding a new requirement by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        try:
            doc = doc_tree.find_document(doc_id)
        except doorstop.DoorstopError:
            raise api.error.DocNotFoundException(f"Document of given UID: {doc_id} was not found.")
        try:
            req = doc.add_item(number=req_number_id)
        except doorstop.DoorstopError:
            raise api.error.InvalidReqIDException(f"Given Req ID: {req_number_id} is invalid.")
        if req_text:
            req.text = req_text
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build document tree.")


def remove_links_to_req(req_id: str, documents: list[doorstop.Document], user_folder: str):
    """
    Function containing logic for removing references to a given subtree requirement from the project document tree. It uses the document tree from the Doorstop API to manage the process of removing an existing subtree by calling the
    relevant Doorstop functions.
    """
    for doc in documents:
        reqs = doc.items
        for req in reqs:
            if str(req.uid) != req_id:
                delete_user_link(str(req.uid), req_id, user_folder)


def delete_user_requirement(doc_id: str, req_uid: str, user_folder: str):
    """
    Function containing the logic for removing a requirement. It uses the tree from the Doorstop API to manage the process of removing an existing requirement by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        doc = doc_tree.find_document(doc_id)
        req = doc.find_item(req_uid)
        remove_links_to_req(req_uid, doc_tree.documents, user_folder)
        req.delete()
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build doorstop tree in the given user folder {user_folder}.")
    except FileNotFoundError:
        raise api.error.ReqNotFoundException(f"{req_uid} does not exist or {doc_id} does not exist.")


def edit_user_requirement(doc_id: str, req_uid: str, req_text: str, user_folder: str):
    """
    Function containing the logic for modifying an existing requirement (modifying the requirement text). It uses the document tree from the Doorstop API to manage the process of modifying an existing requirement by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        doc = doc_tree.find_document(doc_id)
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build doorstop tree in the given user folder {user_folder}.")
    try:
        req = doc.find_item(req_uid)
        req.text = req_text
    except doorstop.DoorstopError:
        raise api.error.ReqNotFoundException(f"{req_uid} does not exist or {doc_id} does not exist.")


def add_user_link(req1_uid: str, req2_uid: str, user_folder: str):
    """
    Function containing the logic to add a reference in an existing requirement to another existing requirement. It uses the document tree from the Doorstop API to manage this process by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        doc_tree.link_items(req1_uid, req2_uid)
    except doorstop.DoorstopError:
        raise api.error.LinkCycleException(f"Attempted to create link cycle.")


def delete_user_link(req1_uid: str, req2_uid: str, user_folder: str):
    """
    Function containing the logic to remove a reference in an existing requirement to another existing requirement. It uses the document tree from the Doorstop API to manage this process by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        doc_tree.unlink_items(req1_uid, req2_uid)
    except doorstop.DoorstopError:
        raise api.error.ReqNotFoundException(f"{req1_uid} does not exist or {req2_uid} does not exist.")


def get_doc_reqs(doc_id: str, user_folder: str) -> list[doorstop.Item] or list:
    """
    Function containing the logic for finding the requirements of an existing document. It uses the document tree from the Doorstop API to manage this process by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        doc_tree = doorstop.build(user_folder)
        doc = doc_tree.find_document(doc_id)
        reqs = doc.items
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build document tree.")
    except FileNotFoundError:
        raise api.error.DocNotFoundException(f"Document of given UID: {doc_id} was not found")
    return reqs


def build_dicts(tree: doorstop.Tree):
    """
    Helper function containing the logic for building the individual document dictionaries included in the document representation returned to the customer. It uses the document tree from the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    doc = tree.document
    doc_dict = {"prefix": str(doc.prefix), "children": []}
    for child in tree.children:
        doc_dict["children"].append(build_dicts(child))
    return doc_dict


def serialize_documents(user_folder: str):
    """
    Function containing the logic for building the document representation returned to the client. It uses the document tree from the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    try:
        data = []
        root_tree = doorstop.build(user_folder)
        if len(root_tree.documents) == 0:
            return data
        data.append(build_dicts(root_tree))
        return data
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build document tree.")


def serialize_doc_reqs(reqs: list[doorstop.Item]) -> list[dict]:
    """
    Function containing the logic for building the requirements dictionaries included in the requirements representation returned to the customer. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    data = []
    for req in reqs:
        data.append({})
        data[-1]["id"] = str(req.uid)
        data[-1]["text"] = req.text
        data[-1]["reviewed"] = req.reviewed
        links = []
        for link in req.links:
            links.append(str(link))
        data[-1]["links"] = links
    return data


def get_all_reqs(user_folder: str):
    """
    Function containing the logic for building the requirements representation returned to the client. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    try:
        root_tree = doorstop.build(user_folder)
        if len(root_tree.documents) == 0:
            return []
        doc = build_dicts(root_tree)
        reqs = get_all_reqs_with_children(user_folder, doc)
        return reqs
    except doorstop.DoorstopError:
        raise api.error.DoorstopException(f"Could not build document tree.")


def get_all_reqs_with_children(user_folder: str, doc):
    """
    Function containing the logic for building the requirements representation returned to the client. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    reqs = []
    req = get_doc_reqs(doc["prefix"], user_folder)
    reqs.extend([(r, doc["prefix"]) for r in req])
    for child in doc["children"]:
        reqs.extend(get_all_reqs_with_children(user_folder, child))
    return reqs


def serialize_all_reqs(reqs):
    """
    Function containing the logic for building the requirements dictionaries included in the requirements representation returned to the customer. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    data = []
    for req_list in reqs:
        req = req_list[0]
        data.append({})
        data[-1]["id"] = str(req.uid)
        data[-1]["text"] = req.text
        data[-1]["reviewed"] = req.reviewed
        data[-1]["docPrefix"] = req_list[1]
        links = []
        for link in req.links:
            links.append(str(link))
        data[-1]["links"] = links
    return data
