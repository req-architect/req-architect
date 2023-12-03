from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import demoapp.restHandlersHelpers

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


def sey_hello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')


@api_view(["POST"])
def add_Document(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    with open("/app/addTest", "w") as filehandle:
        filehandle.writelines(request.data.get("docId"))
    if not serverInfo:
        return Response({'message': 'Unable to add document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.addUserDocument(request.data.get("docId"), request.data.get("parentId"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to add document. Could not build documents tree or root document exists and you need to specify the parent document.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_Requirement(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to add requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.addUserRequirement(request.data.get("docId"), request.data.get("reqNumberId"), request.data.get("reqText"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to add requirement. Invalid document uid or invalid req number or could not build document tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_Document(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to delete document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.deleteUserDocument(request.data.get("docId"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to delete document. Specified document does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_Requirement(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to add requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.deleteUserRequirement(request.data.get("docId"), request.data.get("reqId"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to add requirement. Specified requirement does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["PUT"])
def edit_Requirement(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to modify requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.editUserRequirement(request.data.get("docId"), request.data.get("reqId"), request.data.get("reqText"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to modify requirement. At least one of specified uids is invalid or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["PUT"])
def link_Requirements(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to link requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.addUserLink(request.data.get("req1Id"), request.data.get("req2Id"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to link requirements. At least one of the given requirements does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["PUT"])
def unlink_Requirements(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to unlink requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not demoapp.restHandlersHelpers.deleteUserLink(request.data.get("req1Id"), request.data.get("req2Id"), serverInfo["usersFolder"] + "user/"):
        return Response({'message': 'Unable to unlink requirements. At least one of the given requirements does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'message': 'OK'}, status=status.HTTP_200_OK)


@api_view(["GET"])
def getReqs(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to get requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    reqs = demoapp.restHandlersHelpers.getDocReqs(
        request.data.get("docId"), serverInfo["usersFolder"] + "user/")
    if not reqs:
        return JsonResponse([], safe=False)
    serialized = demoapp.restHandlersHelpers.serializeDocReqs(reqs)
    return JsonResponse(serialized, safe=False)


@api_view(["GET"])
def getDocuments(request):
    serverInfo = demoapp.restHandlersHelpers.readServerInfo(
        "/app/serverInfo.log")
    if not serverInfo:
        return Response({'message': 'Unable to get documents. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    documents = demoapp.restHandlersHelpers.getDocuments(
        serverInfo["usersFolder"] + "user/")
    if not documents:
        return JsonResponse([], safe=False)
    serialized = demoapp.restHandlersHelpers.serializeDocuments(
        documents)
    return JsonResponse(serialized, safe=False)


# @api_view(["PUT"])
# def setDocumentParent(request):
#     serverInfo = demoapp.restHandlersHelpers.readServerInfo(
#         "/app/serverInfo.log")
#     if not serverInfo:
#         return Response({'message': 'Unable to set relation. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     if not demoapp.restHandlersHelpers.setDocumentAsParent(request.data.get("doc1Id"), request.data.get("doc2Id"), serverInfo["usersFolder"] + "user/"):
#         return Response({'message': 'Unable to set realtion. At least one invalid document uid or could not build documents tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     return Response({'message': 'OK'}, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def setDocumentParentToNull(request):
#     serverInfo = demoapp.restHandlersHelpers.readServerInfo(
#         "/app/serverInfo.log")
#     if not serverInfo:
#         return Response({'message': 'Unable to remove parent. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     if not demoapp.restHandlersHelpers.setDocumentParentToNull(request.data.get("doc1Id"), serverInfo["usersFolder"] + "user/"):
#         return Response({'message': 'Unable to remove parent. Invalid document uid or could not build documents tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     return Response({'message': 'OK'}, status=status.HTTP_200_OK)
