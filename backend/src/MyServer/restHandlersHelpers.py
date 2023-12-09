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
    # git.Repo.working_dir = userFolder
    repo = git.Repo.init(path=userFolder)
    return repo


def addUserDocument(docId: str, parentId: str, userFolder: str) -> bool:
    if not checkIfExists(userFolder):
        if not initRepoFolder(userFolder):
            return False
    try:
        docTree = doorstop.build(cwd=userFolder)
        if len(docTree.documents) >= 1 and not parentId:
            return False
        docTree.create_document(
            userFolder + "/" + docId, docId, parent=parentId)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return False


def removeDocTree(tree: doorstop.Tree, docId: str, userFolder: str, rootTree: doorstop.Tree):
    doc = tree.document
    if doc.prefix == docId:
        ToBeRemoved = tree.documents
        ToCheck = [
            document for document in rootTree.documents if document not in ToBeRemoved]
        for document in ToBeRemoved:
            for req in document.items:
                RemoveLinksToReq(req.prefix, ToCheck, userFolder)
        for document in tree.documents:
            rmtree(document.path)
        return
    for child in tree.children:
        removeDocTree(child, docId, userFolder, rootTree)
    return


def deleteUserDocument(docId: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        numberOfDocuments = len(docTree.documents)
        if numberOfDocuments == 0:
            return False
        removeDocTree(docTree, docId, userFolder, docTree)
        docTree = doorstop.build(userFolder)
        if len(docTree.documents) < numberOfDocuments:
            return True
        return False
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return False


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
        return False


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
        req.delete()
        # os.remove(req.path)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return False


def editUserRequirement(docId: str, reqUID: str, reqText: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        req = doc.find_item(reqUID)
        req.text = reqText
        return True
    except doorstop.DoorstopError:
        return False


def addUserLink(req1UID: str, req2UID: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        docTree.link_items(req1UID, req2UID)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
        return False


def deleteUserLink(req1UID: str, req2UID: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(userFolder)
        docTree.unlink_items(req1UID, req2UID)
        return True
    except doorstop.DoorstopError:
        return False
    except FileNotFoundError:
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


def buildDicts(tree: doorstop.Tree):
    doc = tree.document
    dict = {}
    dict["prefix"] = str(doc.prefix)
    dict["children"] = []
    for child in tree.children:
        dict["children"].append(buildDicts(child))
    return dict


def serializeDocuments(userFolder: str):
    try:
        data = []
        rootTree = doorstop.build(userFolder)
        if len(rootTree.documents) == 0:
            return data
        data.append(buildDicts(rootTree))
        return data
    except doorstop.DoorstopError:
        return []


def serializeDocReqs(reqs: list[doorstop.Item]) -> list[dict]:
    data = []
    for req in reqs:
        data.append({})
        data[-1]["id"] = str(req.uid)
        data[-1]["text"] = req.text
        data[-1]["reviewed"] = req.reviewed
    return data
