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
        data.append({})
        data[-1]["prefix"] = str(document.prefix)
        data[-1]["children"] = []
        for child in document.children:
            doc = doorstop.find_document(str(child))
            data[-1]["children"].append(
                buildDicts(doc))
    return data
