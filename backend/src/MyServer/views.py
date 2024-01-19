from typing import Any

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauthlib.oauth2 import AccessDeniedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import MyServer.authHelpers
import MyServer.repoHelpers
import MyServer.repoHelpers
import MyServer.restHandlersHelpers
import MyServer.restHandlersHelpers
from MyServer.authHelpers import requires_jwt_login


# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


"""
Moduł do obsługi żądań klientów odnoszących się do pracy z dokumentami, wymaganiami, repozytoriami i logowaniem.

Poszczególne klasy obsługują typy żądań odnoszące się do zasobów serwera opisanych w nazwie każdej klasy osobno.

Klasy zawierają metody do bsługi konkretnych metod HTTP - typ obsługiwanej metody HTTP jest zawarty w nazwie metody obecnej w danej klasie.

Jeżeli nie wystąpią błędy opisane w module error.py to na żądania klientów zwracane są komunikaty zawierające zasoby serwera (reprezentacje dokumentów, wymagań bądź repozytoriów użytkowników),
komunikaty o statusie 200 potwierdzające poprawne wykonanie operacji.
"""

class ReqView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

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
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.deleteUserRequirement(request.data.get("docId"), request.data.get("reqId"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _editRequirement(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.editUserRequirement(request.data.get("docId"), request.data.get("reqId"), request.data.get("reqText"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _addRequirement(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.addUserRequirement(request.data.get("docId"), request.data.get("reqNumberId"), request.data.get("reqText"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getReqs(self, request):
        doc_id = request.GET.get('docId', '')  # Get docId from query parameters
        if not doc_id:
            return Response({'message': 'Missing docId parameter in the request'}, status=status.HTTP_400_BAD_REQUEST)
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        reqs = MyServer.restHandlersHelpers.getDocReqs(
            request.GET.get("docId"), repoFolder + "/req")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeDocReqs(reqs)
        return JsonResponse(serialized, safe=False)


class DocView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

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
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.addUserDocument(request.data.get("docId"), request.data.get("parentId"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _deleteDocument(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.deleteUserDocument(request.data.get("docId"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    def _getDocuments(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        serialized = MyServer.restHandlersHelpers.serializeDocuments(
            repoFolder + "/req")
        return JsonResponse(serialized, safe=False)


class LinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._addLink(request)

    def _addLink(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.addUserLink(request.data.get("req1Id"), request.data.get("req2Id"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class UnlinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._removeLink(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UnlinkView, self).dispatch(*args, **kwargs)

    def _removeLink(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        MyServer.restHandlersHelpers.deleteUserLink(request.data.get("req1Id"), request.data.get("req2Id"), repoFolder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


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


class GitCommitView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        text = request.data.get("commitText")
        if self._commitAndPush(request, text):
            return Response({'message': "Successfully staged changes in repository!"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Could not publish changes in repository'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def _commitAndPush(self, request, commitText: str):
        authInfo: MyServer.authHelpers.AuthInfo = request.auth
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        providerAPI = MyServer.authHelpers.AuthProviderAPI(authInfo.provider)
        _, userName, userMail = providerAPI.get_identity(authInfo.token)
        if not userMail:
            userMail = providerAPI.getUserMail(authInfo.token)
        return MyServer.repoHelpers.stageChanges(repoFolder, commitText, userName, userMail)


class GetUserReposList(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getUserRepos(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._postChosenRepo(request)

    def _getUserRepos(self, request):
        authInfo: MyServer.authHelpers.AuthInfo = request.auth
        userRepos = MyServer.authHelpers.AuthProviderAPI(authInfo.provider).get_repos(authInfo.token)
        serverUserRepos = MyServer.repoHelpers.getUserServerRepos(userRepos, self._serverRepos)
        return JsonResponse(serverUserRepos, safe=False)

    def _postChosenRepo(self, request):
        authInfo: MyServer.authHelpers.AuthInfo = request.auth
        repoFolder, repoName = MyServer.repoHelpers.getRepoInfo(request)
        repoUrl = self._serverRepos.get(repoName)
        if MyServer.repoHelpers.checkIfExists(repoFolder):
            MyServer.repoHelpers.pullRepo(repoFolder, authInfo.token)
        else:
            MyServer.repoHelpers.cloneRepo(repoFolder, repoUrl, authInfo.token, authInfo.provider)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class AllReqsView(APIView):
    def __init__(self):
        self._serverRepos = MyServer.repoHelpers.getReposFromFile()

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getAllReqs(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AllReqsView, self).dispatch(*args, **kwargs)

    def _getAllReqs(self, request):
        repoFolder, _ = MyServer.repoHelpers.getRepoInfo(request)
        reqs = MyServer.restHandlersHelpers.getAllReqs(repoFolder + "/req")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = MyServer.restHandlersHelpers.serializeAllReqs(reqs)
        return JsonResponse(serialized, safe=False)


class IdentityView(APIView):
    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._getIdentity(request)

    def _getIdentity(self, request):
        authInfo: MyServer.authHelpers.AuthInfo = request.auth
        providerAPI = MyServer.authHelpers.AuthProviderAPI(authInfo.provider)
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
