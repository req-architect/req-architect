from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from enum import Enum
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
import MyServer.restHandlersHelpers
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauthlib.oauth2 import AccessDeniedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import MyServer.authHelpers
import MyServer.restHandlersHelpers
from MyServer.authHelpers import requires_jwt_login


# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style

class STATUS_CODES(Enum):
    LINK_CYCLE_ATTEMPT = 409


class ReqView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        doc_id = request.GET.get('docId', '')  # Get docId from query parameters
        if not doc_id:
            return Response({'message': 'Missing docId parameter in the request'}, status=status.HTTP_400_BAD_REQUEST)

        reqs = MyServer.restHandlersHelpers.getDocReqs(
            request.GET.get("docId"), self._serverInfo["usersFolder"] + "/user")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeDocReqs(reqs)
        return JsonResponse(serialized, safe=False)


class DocView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DocView, self).dispatch(*args, **kwargs)

    @requires_jwt_login
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
            return Response({'message': 'Unable to add document. Could not build documents tree or root document exists and you need to specify the parent document or root document does not exist and you must not specify parentId.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
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
        serialized = MyServer.restHandlersHelpers.serializeDocuments(
            self._serverInfo["usersFolder"] + "/user")
        return JsonResponse(serialized, safe=False)


class LinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    def put(self, request, *args, **kwargs):
        return self._addLink(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LinkView, self).dispatch(*args, **kwargs)

    def _addLink(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to link requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.addUserLink(request.data.get("req1Id"), request.data.get("req2Id"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to link requirements. At least one invalid requirement id or could not build document tree.'}, status=STATUS_CODES.LINK_CYCLE_ATTEMPT.value)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class UnlinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    def put(self, request, *args, **kwargs):
        return self._removeLink(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UnlinkView, self).dispatch(*args, **kwargs)

    def _removeLink(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to unlink requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not MyServer.restHandlersHelpers.deleteUserLink(request.data.get("req1Id"), request.data.get("req2Id"), self._serverInfo["usersFolder"] + "/user"):
            return Response({'message': 'Unable to unlink requirements. At least one invalid requirement id or could not build document tree.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


<<<<<<< backend/src/MyServer/views.py
class LoginCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        provider = MyServer.authHelpers.OAuthProvider[kwargs.get("provider_str").upper()]
        try:
            redirect_url = MyServer.authHelpers.generate_frontend_redirect_url(request.build_absolute_uri(), MyServer.authHelpers.AuthProviderAPI(provider))
        except AccessDeniedError as e:
            return Response({'message': 'Access denied'}, status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponseRedirect(redirect_url)


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        provider = MyServer.authHelpers.OAuthProvider[kwargs.get("provider_str").upper()]
        return HttpResponseRedirect(MyServer.authHelpers.generate_authorization_url(provider))
=======
class AllReqsView(APIView):
    def __init__(self):
        self._serverInfo = MyServer.restHandlersHelpers.readServerInfo(
            "/app/serverInfo.log")

    def get(self, request, *args, **kwargs):
        return self._getAllReqs(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AllReqsView, self).dispatch(*args, **kwargs)

    def _getAllReqs(self, request):
        if not self._serverInfo:
            return Response({'message': 'Unable to get requirements. Server configuration problem'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        reqs = MyServer.restHandlersHelpers.getAllReqs(self._serverInfo["usersFolder"] + "/user")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeAllReqs(reqs)
        return JsonResponse(serialized, safe=False)
>>>>>>> backend/src/MyServer/views.py


def seyHello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')
