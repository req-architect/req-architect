from shutil import rmtree
import MyServer.error
import doorstop

"""
Module to handle communication with the Doorstop API for modifying, adding and deleting requirements and project documents.

It contains functions for adding and removing documents and requirements and for modifying requirements, as well as functions for wrapping the logic for preparing
representation of existing documents and requirements to customers.
"""

def addUserDocument(docId: str, parentId: str, userFolder: str):
    """
    Function containing the logic for adding a document. It uses the document tree from the Doorstop API to manage the process of adding a new document by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client via the
    appropriate exceptions.
    """
    try:
        docTree = doorstop.build(cwd=userFolder)
        if len(docTree.documents) >= 1 and not parentId:
            raise MyServer.error.NoParentSpecifiedException(f"parentID must be specified for the given document.")
        if len(docTree.documents) == 0 and parentId:
            raise MyServer.error.ParentOfEmptyTreeSpecifiedException()
        docName = userFolder + "/" + docId
        docTree.create_document(
            docName, docId, parent=parentId)
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build document tree.")
    except FileNotFoundError:
        raise MyServer.error.DoorstopException(f"User folder {userFolder} was not found.")

def removeDocTree(tree: doorstop.Tree, docId: str, userFolder: str, rootTree: doorstop.Tree):
    """
    Function containing the logic for removing a specific subtree from the project document tree. It uses the tree from the Doorstop API to manage the process of deleting an existing subtree by calling the
    appropriate Doorstop functions.
    """
    doc = tree.document
    if doc.prefix == docId:
        ToBeRemoved = tree.documents
        ToCheck = [
            document for document in rootTree.documents if document not in ToBeRemoved]
        for document in ToBeRemoved:
            for req in document.items:
                RemoveLinksToReq(str(req.uid), ToCheck, userFolder)
        for document in tree.documents:
            rmtree(document.path)
        return
    for child in tree.children:
        removeDocTree(child, docId, userFolder, rootTree)
    return


def deleteUserDocument(docId: str, userFolder: str):
    """
    Function containing the logic for deleting a document. Uses the document tree from the Doorstop API to manage the process of deleting an existing document by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        numberOfDocuments = len(docTree.documents)
        if numberOfDocuments == 0:
            raise MyServer.error.EmptyDocumentTreeException(f"No documents were created yet.")
        try:
            doc = docTree.find_document(docId)
        except doorstop.DoorstopError:
            raise MyServer.error.DocNotFoundException(f"Document of given UID: {docId} was not found.")
        removeDocTree(docTree, docId, userFolder, docTree)
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build document tree.")
        


def addUserRequirement(docId: str, reqNumberId: int, reqText: str, userFolder: str):
    """
    Function containing the logic for adding a requirement. It uses the document tree from the Doorstop API to manage the process of adding a new requirement by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        try:
            doc = docTree.find_document(docId)
        except doorstop.DoorstopError:
            raise MyServer.error.DocNotFoundException(f"Document of given UID: {docId} was not found.")
        try:
            req = doc.add_item(number=reqNumberId)
        except doorstop.DoorstopError:
            raise MyServer.error.InvalidReqIDException(f"Given Req ID: {reqNumberId} is invalid.")
        if reqText:
            req.text = reqText
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build document tree.")


def RemoveLinksToReq(reqId: str, documents: list[doorstop.Document], userFolder: str):
    """
    Function containing logic for removing references to a given subtree requirement from the project document tree. It uses the document tree from the Doorstop API to manage the process of removing an existing subtree by calling the
    relevant Doorstop functions.
    """
    for doc in documents:
        reqs = doc.items
        for req in reqs:
            if str(req.uid) != reqId:
                deleteUserLink(str(req.uid), reqId, userFolder)


def deleteUserRequirement(docId: str, reqUID: str, userFolder: str):
    """
    Function containing the logic for removing a requirement. It uses the tree from the Doorstop API to manage the process of removing an existing requirement by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        req = doc.find_item(reqUID)
        RemoveLinksToReq(reqUID, docTree.documents, userFolder)
        req.delete()
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build doorstop tree in the given user folder {userFolder}.")
    except FileNotFoundError:
        raise MyServer.error.ReqNotFoundException(f"{reqUID} does not exist or {docId} does not exist.")


def editUserRequirement(docId: str, reqUID: str, reqText: str, userFolder: str):
    """
    Function containing the logic for modifying an existing requirement (modifying the requirement text). It uses the document tree from the Doorstop API to manage the process of modifying an existing requirement by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build doorstop tree in the given user folder {userFolder}.")
    try:
        req = doc.find_item(reqUID)
        req.text = reqText
    except doorstop.DoorstopError:
        raise MyServer.error.ReqNotFoundException(f"{reqUID} does not exist or {docId} does not exist.")


def addUserLink(req1UID: str, req2UID: str, userFolder: str):
    """
    Function containing the logic to add a reference in an existing requirement to another existing requirement. It uses the document tree from the Doorstop API to manage this process by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        docTree.link_items(req1UID, req2UID)
    except doorstop.DoorstopError:
        raise MyServer.error.LinkCycleException(f"Attempted to create link cycle.")

def deleteUserLink(req1UID: str, req2UID: str, userFolder: str):
    """
    Function containing the logic to remove a reference in an existing requirement to another existing requirement. It uses the document tree from the Doorstop API to manage this process by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        docTree.unlink_items(req1UID, req2UID)
    except doorstop.DoorstopError:
        raise MyServer.error.ReqNotFoundException(f"{req1UID} does not exist or {req2UID} does not exist.")


def getDocReqs(docId: str, userFolder: str) -> list[doorstop.Item] or list:
    """
    Function containing the logic for finding the requirements of an existing document. It uses the document tree from the Doorstop API to manage this process by calling the
    appropriate Doorstop functions. If an error occurs during this process, an appropriate message is created and returned to the client
    via appropriate exceptions.
    """
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        reqs = doc.items
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build document tree.")
    except FileNotFoundError:
        raise MyServer.error.DocNotFoundException(f"Document of given UID: {docId} was not found")
    return reqs


def buildDicts(tree: doorstop.Tree):
    """
    Helper function containing the logic for building the individual document dictionaries included in the document representation returned to the customer. It uses the document tree from the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    doc = tree.document
    dict = {}
    dict["prefix"] = str(doc.prefix)
    dict["children"] = []
    for child in tree.children:
        dict["children"].append(buildDicts(child))
    return dict


def serializeDocuments(userFolder: str):
    """
    Function containing the logic for building the document representation returned to the client. It uses the document tree from the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    try:
        data = []
        rootTree = doorstop.build(userFolder)
        if len(rootTree.documents) == 0:
            return data
        data.append(buildDicts(rootTree))
        return data
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build document tree.")


def serializeDocReqs(reqs: list[doorstop.Item]) -> list[dict]:
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


def getAllReqs(userFolder: str):
    """
    Function containing the logic for building the requirements representation returned to the client. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    try:
        rootTree = doorstop.build(userFolder)
        if len(rootTree.documents) == 0:
            return []
        doc = buildDicts(rootTree)
        reqs = getAllReqsWithChildren(userFolder, doc)
        return reqs
    except doorstop.DoorstopError:
        raise MyServer.error.DoorstopException(f"Could not build document tree.")

def getAllReqsWithChildren(userFolder: str, doc):
    """
    Function containing the logic for building the requirements representation returned to the client. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    reqs = []
    req = getDocReqs(doc["prefix"], userFolder)
    reqs.extend([(r, doc["prefix"]) for r in req])
    for child in doc["children"]:
        reqs.extend(getAllReqsWithChildren(userFolder, child))
    return reqs

def serializeAllReqs(reqs):
    """
    Function containing the logic for building the requirements dictionaries included in the requirements representation returned to the customer. It uses the Doorstop API to manage this process by calling the
    relevant Doorstop functions.
    """
    data = []
    for reqlist in reqs:
        req = reqlist[0]
        data.append({})
        data[-1]["id"] = str(req.uid)
        data[-1]["text"] = req.text
        data[-1]["reviewed"] = req.reviewed
        data[-1]["docPrefix"] = reqlist[1]
        links = []
        for link in req.links:
            links.append(str(link))
        data[-1]["links"] = links
    return data
