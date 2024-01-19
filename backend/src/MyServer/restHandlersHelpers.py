from shutil import rmtree
import MyServer.error
import doorstop

"""
Moduł do obsługi komunikacji z API Doorstop w celu modyfikacji wymagań i dokumnetów projetków oraz ich dodawania i usuwania.

Zawiera funkcje do dodawnia i usuwania dokumnetów i wymagań oraz do modyfikacji wymagań a także funkcje opakowujące logikę przygotowywania
reprezentacji istniejących dokumentów i wymagań do klientów.
"""

def addUserDocument(docId: str, parentId: str, userFolder: str):
    """
    Funkcja zawierająca logikę dodawania dokumnetu. Korzysta z drzewa dokumnetów z API Doorstop do zarządzania procesem dodawnia nowego dokumentu wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
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
    Funkcja zawierająca logikę usuwania konkretnego poddrzewa z drzewa dokumentów projektu. Korzysta z drzewa z API Doorstop do zarządzania procesem usuwania istniejącego poddrzewa wywołując
    odpowiednie funkcje Doorstopa.
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
    Funkcja zawierająca logikę usuwania dokumentu. Korzysta z drzewa dokumentów z API Doorstop do zarządzania procesem usuwania istniejącego dokumentu wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
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
    Funkcja zawierająca logikę dodawania wymagania. Korzysta z drzewa dokumentów z API Doorstop do zarządzania procesem dodawnia nowego wymagania wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
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
    Funkcja zawierająca logikę usuwania odniesień do danego wymagania poddrzewa z drzewa dokumentów projektu. Korzysta z drzewa dokumentów z API Doorstop do zarządzania procesem usuwania istniejącego poddrzewa wywołując
    odpowiednie funkcje Doorstopa.
    """
    for doc in documents:
        reqs = doc.items
        for req in reqs:
            if str(req.uid) != reqId:
                deleteUserLink(str(req.uid), reqId, userFolder)


def deleteUserRequirement(docId: str, reqUID: str, userFolder: str):
    """
    Funkcja zawierająca logikę usuwania wymagania. Korzysta z drzewa z API Doorstop do zarządzania procesem usuwania istniejącego wymagania wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
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
    Funkcja zawierająca logikę modyfikacji istniejącego wymagania (modyfikacja tekstu wymagania). Korzysta z drzewa dokumentów z API Doorstop do zarządzania procesem modyfikacji istniejącego wymagania wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
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
    Funkcja zawierająca logikę dodawnia odniesienia w istniejącym wymaganiu do innego istniejącego wymagania. Korzysta z drzewa dokumentów z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
    """
    try:
        docTree = doorstop.build(userFolder)
        docTree.link_items(req1UID, req2UID)
    except doorstop.DoorstopError:
        raise MyServer.error.LinkCycleException(f"Attempted to create link cycle.")

def deleteUserLink(req1UID: str, req2UID: str, userFolder: str):
    """
    Funkcja zawierająca logikę usuwania odniesienia w istniejącym wymaganiu do innego istniejącego wymagania. Korzysta z drzewa dokumentów z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
    """
    try:
        docTree = doorstop.build(userFolder)
        docTree.unlink_items(req1UID, req2UID)
    except doorstop.DoorstopError:
        raise MyServer.error.ReqNotFoundException(f"{req1UID} does not exist or {req2UID} does not exist.")


def getDocReqs(docId: str, userFolder: str) -> list[doorstop.Item] or list:
    """
    Funkcja zawierająca logikę znajdowania wymagań istniejącego dokumentu. Korzysta z drzewa dokumentów z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa. W przypadku wystąpienia błędu podczas tego procesu tworzony jest i zwracany odpowiedni komunikat do klienta za
    pośrednictwem odpowiednich wyjątków.
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
    Funkcja pomocnicza zawierająca logikę budowy poszczególnych słowników dokumentów wchodzących w skład reprezentacji dokumentów zwracanej do klienta. Korzysta z drzewa dokumentów z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa.
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
    Funkcja zawierająca logikę budowy reprezentacji dokumentów zwracanej do klienta. Korzysta z drzewa dokumentów z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa.
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
    Funkcja zawierająca logikę budowy słowników wymagań wchodzących w skład reprezentacji wymagań zwracanej do klienta. Korzysta z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa.
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
    Funkcja zawierająca logikę budowy reprezentacji wymagań zwracanej do klienta. Korzysta z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa.
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
    Funkcja zawierająca logikę budowy reprezentacji wymagań zwracanej do klienta. Korzysta z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa.
    """
    reqs = []
    req = getDocReqs(doc["prefix"], userFolder)
    reqs.extend([(r, doc["prefix"]) for r in req])
    for child in doc["children"]:
        reqs.extend(getAllReqsWithChildren(userFolder, child))
    return reqs

def serializeAllReqs(reqs):
    """
    Funkcja zawierająca logikę budowy słowników wymagań wchodzących w skład reprezentacji wymagań zwracanej do klienta. Korzysta z API Doorstop do zarządzania tym procesem wywołując
    odpowiednie funkcje Doorstopa.
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
