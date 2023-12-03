from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import demoapp.restHandlersHelpers
import doorstop
import os

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


def sey_hello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')


@api_view(["POST"])
def add_Document(request):
    if request.method == "POST":
        data = request.data
        docId = data.get("docId")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.addUserDocument(docId, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to add document. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to add document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_Requirement(request):
    if request.method == "POST":
        data = request.data
        docId = data.get("docId")
        reqNumberId = data.get("reqNumberId")
        reqText = data.get("reqText")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.addUserRequirement(docId, reqNumberId, reqText, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to add requirement. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to add requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_Document(request):
    if request.method == "DELETE":
        data = request.data
        docId = data.get("docId")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.deleteUserDocument(docId, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to delete document. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to delete document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_Requirement(request):
    if request.method == "DELETE":
        data = request.data
        docId = data.get("docId")
        reqId = data.get("reqId")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.deleteUserRequirement(docId, reqId, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to add requirement. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to add requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def edit_Requirement(request):
    if request.method == "PUT":
        data = request.data
        docId = data.get("docId")
        reqId = data.get("reqId")
        reqText = data["reqText"]
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.editUserRequirement(docId, reqId, reqText, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to modify requirement. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to modify requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def link_Requirements(request):
    if request.method == "PUT":
        data = request.data
        req1Id = data.get("req1Id")
        req2Id = data.get("req2Id")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.addUserLink(req1Id, req2Id, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to link requirements. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to link requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def unlink_Requirements(request):
    if request.method == "PUT":
        data = request.data
        req1Id = data.get("req1Id")
        req2Id = data.get("req2Id")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            if not demoapp.restHandlersHelpers.deleteUserLink(req1Id, req2Id, serverInfo["rootFolder"] + "/user"):
                return Response({'message': 'Unable to unlink requirements. Internal problems'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Unable to unlink requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getReqs(request):
    if request.method == "GET":
        data = request.data
        docId = data.get("docId")
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            reqs = demoapp.restHandlersHelpers.getDocReqs(
                docId, serverInfo["rootFolder"] + "/user")
            if not reqs:
                return JsonResponse([], safe=False)
            return JsonResponse(reqs, safe=False)
        else:
            return Response({'message': 'Unable to get requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getDocuments(request):
    if request.method == "GET":
        serverInfo = demoapp.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")
        if serverInfo:
            documents = demoapp.restHandlersHelpers.getDocuments(
                serverInfo["rootFolder"] + "/user")
            if not documents:
                return JsonResponse([], safe=False)
            serialized = demoapp.restHandlersHelpers.serializeDocuments(
                documents)
            return JsonResponse(serialized, safe=False)
        else:
            return Response({'message': 'Unable to get documents. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)
