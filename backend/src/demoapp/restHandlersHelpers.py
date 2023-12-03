import doorstop


def getDocuments():
    tree = doorstop.build()
    return tree.documents


def buildDicts(document):
    dict = {}
    dict["prefix"] = str(document.prefix)
    dict["children"] = []
    for child in document.children:
        doc = doorstop.find_document(str(child))
        dict["children"].append(buildDicts(doc))
    return dict


def serializeDocuments(documents):
    data = []
    for document in documents:
        if not document.parent:
            data.append(buildDicts(document))
    return data
