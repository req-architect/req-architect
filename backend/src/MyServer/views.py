from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import MyServer.restHandlersHelpers
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


class ReqView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReqView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._getReqs(request)

    def post(self, request, *args, **kwargs):
        return self._addRequirement(request)

    def delete(self, request, *args, **kwargs):
        return self._deleteRequirement(request)

    def put(self, request, *args, **kwargs):
        return self._editRequirement(request)

    def _deleteRequirement(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to delete requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.deleteUserRequirement(request.data.get("docId"), request.data.get("reqId"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to delete requirement. Specified requirement does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _editRequirement(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to modify requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.editUserRequirement(request.data.get("docId"), request.data.get("reqId"), request.data.get("reqText"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to modify requirement. At least one of specified uids is invalid or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _addRequirement(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to add requirement. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.addUserRequirement(request.data.get("docId"), request.data.get("reqNumberId"), request.data.get("reqText"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to add requirement. Invalid document uid or invalid req number or could not build document tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getReqs(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to get requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        reqs = MyServer.restHandlersHelpers.getDocReqs(
            request.data.get("docId"), self._serverInfo["usersFolder"] + "/user")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeDocReqs(reqs)
        return JsonResponse(serialized, safe=False)


class DocView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DocView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._getDocuments(request)

    def post(self, request, *args, **kwargs):
        return self._addDocument(request)

    def delete(self, request, *args, **kwargs):
        return self._deleteDocument(request)

    def _addDocument(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to add document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.addUserDocument(request.data.get("docId"), request.data.get("parentId"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to add document. Could not build documents tree or root document exists and you need to specify the parent document.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _deleteDocument(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to delete document. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.deleteUserDocument(request.data.get("docId"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to delete document. Specified document does not exist or could not build document tree'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getDocuments(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to get documents. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        documents = MyServer.restHandlersHelpers.getDocuments(
            self._serverInfo["usersFolder"] + "/user")
        if not documents:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeDocuments(
            documents, self._serverInfo["usersFolder"] + "/user")
        return JsonResponse(serialized, safe=False)


def seyHello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')


# @api_view(["PUT"])
# def setDocumentParent(request):
#     serverInfo = MyServer.restHandlersHelpers.readServerInfo(
#         "/app/serverInfo.log")
#     if not serverInfo:
#         return Response({'message': 'Unable to set relation. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     if not MyServer.restHandlersHelpers.setDocumentAsParent(request.data.get("doc1Id"), request.data.get("doc2Id"), serverInfo["usersFolder"] + "user/"):
#         return Response({'message': 'Unable to set realtion. At least one invalid document uid or could not build documents tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     return Response({'message': 'OK'}, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def setDocumentParentToNull(request):
#     serverInfo = MyServer.restHandlersHelpers.readServerInfo(
#         "/app/serverInfo.log")
#     if not serverInfo:
#         return Response({'message': 'Unable to remove parent. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     if not MyServer.restHandlersHelpers.setDocumentParentToNull(request.data.get("doc1Id"), serverInfo["usersFolder"] + "user/"):
#         return Response({'message': 'Unable to remove parent. Invalid document uid or could not build documents tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     return Response({'message': 'OK'}, status=status.HTTP_200_OK)
