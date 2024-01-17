from shutil import rmtree
import MyServer.error
import doorstop


def addUserDocument(docId: str, parentId: str, userFolder: str) -> bool:
    try:
        docTree = doorstop.build(cwd=userFolder)
        if len(docTree.documents) >= 1 and not parentId:
            return False
        if len(docTree.documents) == 0 and parentId:
            return False
        docName = userFolder + "/" + docId
        docTree.create_document(
            docName, docId, parent=parentId)
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
                RemoveLinksToReq(str(req.uid), ToCheck, userFolder)
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
        req = doc.add_item(number=reqNumberId)
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
    except doorstop.DoorstopError as d:
        raise MyServer.error.DoorstopException(str(d))
    except FileNotFoundError:
        raise MyServer.error.LinkCycleException()


def getDocReqs(docId: str, userFolder: str) -> list[doorstop.Item] or list or None:
    try:
        docTree = doorstop.build(userFolder)
        doc = docTree.find_document(docId)
        reqs = doc.items
    except doorstop.DoorstopError:
        return []
    except FileNotFoundError:
        return []
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
    except FileNotFoundError:
        return []


def serializeDocReqs(reqs: list[doorstop.Item]) -> list[dict]:
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
    try:
        rootTree = doorstop.build(userFolder)
        if len(rootTree.documents) == 0:
            return []
        doc = buildDicts(rootTree)
        reqs = getAllReqsWithChildren(userFolder, doc)
        return reqs
    except doorstop.DoorstopError:
        return []
    except FileNotFoundError:
        return []

def getAllReqsWithChildren(userFolder: str, doc):
    reqs = []
    req = getDocReqs(doc["prefix"], userFolder)
    reqs.extend([(r, doc["prefix"]) for r in req])
    for child in doc["children"]:
        reqs.extend(getAllReqsWithChildren(userFolder, child))
    return reqs

def serializeAllReqs(reqs):
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
