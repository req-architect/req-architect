import doorstop
import os
import git
from shutil import rmtree


def readServerInfo(filename: str):
    serverInfo = {}
    try:
        with open(filename, "r") as filehandle:
            for line in filehandle:
                info = line.split()
                serverInfo[info[0]] = info[1]
        return serverInfo
    except FileNotFoundError:
        return None
    except IndexError:
        return None


def checkIfExists(userFolder: str) -> bool:
    if os.path.exists(userFolder):
        return True
    return False


def initRepoFolder(userFolder: str) -> git.Repo:
    os.makedirs(userFolder)
    # os.chdir(userFolder)
    git.Repo.working_dir = userFolder
    repo = git.Repo.init(path=userFolder)
    return repo


# def setWorkingDirectory(userFolder: str) -> bool:
#     if not checkIfExists(userFolder):
#         return False
#     else:
#         os.chdir(userFolder)
#         return True


# def setDocumentAsParent(doc1Id: str, doc2Id: str, userFolder: str) -> bool:
#     if not setWorkingDirectory(userFolder):
#         return False
#     try:
#         docTree = doorstop.build()
#         doc1 = docTree.find_document(doc1Id)
#         doc1.parent = doc2Id
#         return True
#     except doorstop.DoorstopError:
#         return False


# def setDocumentParentToNull(doc1Id: str, userFolder: str) -> bool:
#     if not setWorkingDirectory(userFolder):
#         return False
#     try:
#         docTree = doorstop.build()
#         doc1 = docTree.find_document(doc1Id)
#         doc1.parent = None
#         return True
#     except doorstop.DoorstopError:
#         return False


def addUserDocument(docId: str, parentId: str, userFolder: str) -> bool:
    if not checkIfExists(userFolder):
        if not initRepoFolder(userFolder):
            return False
    try:
        docTree = doorstop.build(cwd=userFolder)
        docTree.create_document(
            userFolder + "/" + docId, docId, parent=parentId)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return None


def DeleteChildren(children: list[doorstop.Document], userFolder: str):
    for child in children:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(child)
        grandChildren = doc.children
        for req in doc.items:
            RemoveLinksToReq(str(req.uid), docTree.documents, userFolder)
        for grandChild in grandChildren:
            DeleteChildren(grandChild.children)
        doc.delete()
        rmtree(doc.path)


def deleteUserDocument(docId: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        DeleteChildren(doc.children, userFolder)
        for req in doc.items:
            RemoveLinksToReq(str(req.uid), docTree.documents, userFolder)
        doc.delete()
        rmtree(doc.path)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return None


def addUserRequirement(docId: str, reqNumberId: int, reqText: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        req = doc.add_item(reqNumberId)
        if reqText:
            req.text = reqText
        return True
    except doorstop.DoorstopError:
        return False
    except TypeError:
        return False
    except FileNotFoundError:
        return None


def RemoveLinksToReq(reqId: str, documents: list[doorstop.Document], userFolder: str):
    for doc in documents:
        reqs = doc.items
        for req in reqs:
            if str(req.uid) != reqId:
                deleteUserLink(str(req.uid), reqId, userFolder)


def deleteUserRequirement(docId: str, reqUID: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        req = doc.find_item(reqUID)
        RemoveLinksToReq(reqUID, docTree.documents, userFolder)
        # req.delete()
        os.remove(req.path)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return None


def editUserRequirement(docId: str, reqUID: str, reqText: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        req = doc.find_item(reqUID)
        req.text = reqText
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return None


def addUserLink(req1UID: str, req2UID: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        docTree.link_items(req1UID, req2UID)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return None


def deleteUserLink(req1UID: str, req2UID: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        docTree.unlink_items(req1UID, req2UID)
        return True
    except doorstop.DoorstopError:
        return False


def getDocReqs(docId: str, userFolder: str) -> list[doorstop.Item] or list or None:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        reqs = doc.items
    except doorstop.DoorstopError:
        return None
    except FileNotFoundError:
        return None
    return reqs


def getDocuments(userFolder: str) -> list[doorstop.Document] or list or None:
    try:
        docTree = doorstop.build(userFolder)
        return docTree.documents
    except doorstop.DoorstopError:
        return None
    except FileNotFoundError:
        return None


def buildDicts(document: doorstop.Document, userFolder: str) -> dict:
    dict = {}
    dict["prefix"] = str(document.prefix)
    dict["children"] = []
    docTree = doorstop.build(userFolder)
    for child in document.children:
        doc = docTree.find_document(str(child))
        dict["children"].append(buildDicts(doc, userFolder))
    return dict


def serializeDocuments(documents: list[doorstop.Document], userFolder: str) -> list[dict]:
    data = []
    for document in documents:
        if not document.parent:
            data.append(buildDicts(document, userFolder))
    return data


def serializeDocReqs(reqs: list[doorstop.Item]) -> list[dict]:
    data = []
    for req in reqs:
        data.append({})
        data[-1]["id"] = str(req.uid)
        data[-1]["text"] = req.text
        data[-1]["reviewed"] = req.reviewed
    return data
