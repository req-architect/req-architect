from typing import Any

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauthlib.oauth2 import AccessDeniedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import api.authHelpers
import api.repoHelpers
import api.repoHelpers
import api.restHandlersHelpers
import api.restHandlersHelpers
from api.authHelpers import requires_jwt_login


# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


"""
A module for handling client requests relating to working with documents, requirements, repositories and logging.

The individual classes support the types of requests relating to server resources described in the name of each class separately.

Classes contain methods to bservice specific HTTP methods - the type of HTTP method supported is contained in the name of the method present in the class.

If no errors described in the error.py module occur, messages containing server resources (representations of documents, requirements or user repositories) are returned to client requests,
status 200 messages confirming the correct execution of the operation.
"""

class ReqView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReqView, self).dispatch(*args, **kwargs)

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getReqs(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._addRequirement(request)

    @requires_jwt_login
    def delete(self, request, *args, **kwargs):
        return self._deleteRequirement(request)

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._editRequirement(request)

    def _deleteRequirement(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.deleteUserRequirement(request.data.get("docId"), request.data.get("reqId"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _editRequirement(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.editUserRequirement(request.data.get("docId"), request.data.get("reqId"), request.data.get("reqText"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _addRequirement(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.addUserRequirement(request.data.get("docId"), request.data.get("reqNumberId"), request.data.get("reqText"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getReqs(self, request):
        doc_id = request.GET.get('docId', '')  # Get docId from query parameters
        if not doc_id:
            return Response({'message': 'Missing docId parameter in the request'}, status=status.HTTP_400_BAD_REQUEST)
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        reqs = api.restHandlersHelpers.getDocReqs(
            request.GET.get("docId"), repoFolder + "/req")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = api.restHandlersHelpers.serializeDocReqs(reqs)
        return JsonResponse(serialized, safe=False)


class DocView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DocView, self).dispatch(*args, **kwargs)

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getDocuments(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._addDocument(request)

    @requires_jwt_login
    def delete(self, request, *args, **kwargs):
        return self._deleteDocument(request)

    def _addDocument(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.addUserDocument(request.data.get("docId"), request.data.get("parentId"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _deleteDocument(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.deleteUserDocument(request.data.get("docId"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getDocuments(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        serialized = api.restHandlersHelpers.serializeDocuments(
            repoFolder + "/req")
        return JsonResponse(serialized, safe=False)


class LinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._addLink(request)

    def _addLink(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.addUserLink(request.data.get("req1Id"), request.data.get("req2Id"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class UnlinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._removeLink(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UnlinkView, self).dispatch(*args, **kwargs)

    def _removeLink(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        api.restHandlersHelpers.deleteUserLink(request.data.get("req1Id"), request.data.get("req2Id"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class LoginCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        provider = api.authHelpers.OAuthProvider[kwargs.get("provider_str").upper()]
        try:
            redirect_url = api.authHelpers.generate_frontend_redirect_url(request.build_absolute_uri(), api.authHelpers.AuthProviderAPI(provider))
        except AccessDeniedError as e:
            return Response({'message': 'Access denied'}, status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponseRedirect(redirect_url)


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        provider = api.authHelpers.OAuthProvider[kwargs.get("provider_str").upper()]
        return HttpResponseRedirect(api.authHelpers.generate_authorization_url(provider))


class GitCommitView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        text = request.data.get("commitText")
        if self._commitAndPush(request, text):
            return Response({'message': "Successfully staged changes in repository!"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Could not publish changes in repository'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def _commitAndPush(self, request, commitText: str):
        authInfo: api.authHelpers.AuthInfo = request.auth
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        providerAPI = api.authHelpers.AuthProviderAPI(authInfo.provider)
        _, userName, userMail = providerAPI.get_identity(authInfo.token)
        if not userMail:
            userMail = providerAPI.getUserMail(authInfo.token)
        return api.repoHelpers.stageChanges(repoFolder, commitText, userName, userMail)


class GetUserReposList(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getUserRepos(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._postChosenRepo(request)

    def _getUserRepos(self, request):
        authInfo: api.authHelpers.AuthInfo = request.auth
        userRepos = api.authHelpers.AuthProviderAPI(authInfo.provider).get_repos(authInfo.token)
        serverUserRepos = api.repoHelpers.getUserServerRepos(userRepos, self._serverRepos)
        return JsonResponse(serverUserRepos, safe=False)

    def _postChosenRepo(self, request):
        authInfo: api.authHelpers.AuthInfo = request.auth
        repoFolder, repoName = api.repoHelpers.getRepoInfo(request)
        repoUrl = self._serverRepos.get(repoName)
        if api.repoHelpers.checkIfExists(repoFolder):
            api.repoHelpers.pullRepo(repoFolder, authInfo.token)
        else:
            api.repoHelpers.cloneRepo(repoFolder, repoUrl, authInfo.token, authInfo.provider)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class AllReqsView(APIView):
    def __init__(self):
        self._serverRepos = api.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getAllReqs(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AllReqsView, self).dispatch(*args, **kwargs)

    def _getAllReqs(self, request):
        repoFolder, _ = api.repoHelpers.getRepoInfo(request)
        reqs = api.restHandlersHelpers.getAllReqs(repoFolder + "/req")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = api.restHandlersHelpers.serializeAllReqs(reqs)
        return JsonResponse(serialized, safe=False)


class IdentityView(APIView):
    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getIdentity(request)

    def _getIdentity(self, request):
        authInfo: api.authHelpers.AuthInfo = request.auth
        providerAPI = api.authHelpers.AuthProviderAPI(authInfo.provider)
        uid, login, email = providerAPI.get_identity(authInfo.token)
        if not email:
            email = providerAPI.getUserMail(authInfo.token)
        return JsonResponse({"uid": uid,
                             "login": login,
                             "email": email,
                             "provider": authInfo.provider.name.lower()})


def seyHello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')
