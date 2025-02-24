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
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReqView, self).dispatch(*args, **kwargs)

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._get_reqs(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._add_requirement(request)

    @requires_jwt_login
    def delete(self, request, *args, **kwargs):
        return self._delete_requirement(request)

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._edit_requirement(request)

    @staticmethod
    def _delete_requirement(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.delete_user_requirement(request.data.get("docId"), request.data.get("reqId"), repo_folder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @staticmethod
    def _edit_requirement(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.edit_user_requirement(request.data.get("docId"), request.data.get("reqId"), request.data.get("reqText"), repo_folder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @staticmethod
    def _add_requirement(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.add_user_requirement(request.data.get("docId"), request.data.get("reqNumberId"), request.data.get("reqText"), repo_folder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @staticmethod
    def _get_reqs(request):
        doc_id = request.GET.get('docId', '')  # Get docId from query parameters
        if not doc_id:
            return Response({'message': 'Missing docId parameter in the request'}, status=status.HTTP_400_BAD_REQUEST)
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        reqs = api.restHandlersHelpers.get_doc_reqs(
            request.GET.get("docId"), repo_folder + "/req")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = api.restHandlersHelpers.serialize_doc_reqs(reqs)
        return JsonResponse(serialized, safe=False)


class DocView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DocView, self).dispatch(*args, **kwargs)

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._get_documents(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._add_document(request)

    @requires_jwt_login
    def delete(self, request, *args, **kwargs):
        return self._delete_document(request)

    @staticmethod
    def _add_document(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.add_user_document(request.data.get("docId"), request.data.get("parentId"), repo_folder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @staticmethod
    def _delete_document(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.delete_user_document(request.data.get("docId"), repo_folder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @staticmethod
    def _get_documents(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        serialized = api.restHandlersHelpers.serialize_documents(
            repo_folder + "/req")
        return JsonResponse(serialized, safe=False)


class LinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._add_link(request)

    @staticmethod
    def _add_link(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.add_user_link(request.data.get("req1Id"), request.data.get("req2Id"), repo_folder + "/req")
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class UnlinkView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @requires_jwt_login
    def put(self, request, *args, **kwargs):
        return self._remove_link(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UnlinkView, self).dispatch(*args, **kwargs)

    @staticmethod
    def _remove_link(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        api.restHandlersHelpers.delete_user_link(request.data.get("req1Id"), request.data.get("req2Id"), repo_folder + "/req")
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
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        text = request.data.get("commitText")
        if self._commit_and_push(request, text):
            return Response({'message': "Successfully staged changes in repository!"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Could not publish changes in repository'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @staticmethod
    def _commit_and_push(request, commit_text: str):
        auth_info: api.authHelpers.AuthInfo = request.auth
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        provider_api = api.authHelpers.AuthProviderAPI(auth_info.provider)
        _, user_name, user_mail = provider_api.get_identity(auth_info.token)
        if not user_mail:
            user_mail = provider_api.get_user_mail(auth_info.token)
        return api.repoHelpers.stage_changes(repo_folder, commit_text, user_name, user_mail)


class GetUserReposList(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._get_user_repos(request)

    @requires_jwt_login
    def post(self, request, *args, **kwargs):
        return self._post_chosen_repo(request)

    def _get_user_repos(self, request):
        auth_info: api.authHelpers.AuthInfo = request.auth
        user_repos = api.authHelpers.AuthProviderAPI(auth_info.provider).get_repos(auth_info.token)
        server_user_repos = api.repoHelpers.get_user_server_repos(user_repos, self._serverRepos)
        return JsonResponse(server_user_repos, safe=False)

    def _post_chosen_repo(self, request):
        auth_info: api.authHelpers.AuthInfo = request.auth
        repo_folder, repo_name = api.repoHelpers.get_repo_info(request)
        repo_url = self._serverRepos.get(repo_name)
        if api.repoHelpers.check_if_exists(repo_folder):
            api.repoHelpers.pull_repo(repo_folder, auth_info.token)
        else:
            api.repoHelpers.clone_repo(repo_folder, repo_url, auth_info.token, auth_info.provider)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)


class AllReqsView(APIView):
    def __init__(self):
        self._serverRepos = api.repoHelpers.get_repos_from_file()

    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._get_all_reqs(request)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AllReqsView, self).dispatch(*args, **kwargs)

    @staticmethod
    def _get_all_reqs(request):
        repo_folder, _ = api.repoHelpers.get_repo_info(request)
        reqs = api.restHandlersHelpers.get_all_reqs(repo_folder + "/req")
        if not reqs:
            return JsonResponse([], safe=False)
        serialized = api.restHandlersHelpers.serialize_all_reqs(reqs)
        return JsonResponse(serialized, safe=False)


class IdentityView(APIView):
    @requires_jwt_login
    def get(self, request, *args, **kwargs):
        return self._get_identity(request)

    @staticmethod
    def _get_identity(request):
        auth_info: api.authHelpers.AuthInfo = request.auth
        provider_api = api.authHelpers.AuthProviderAPI(auth_info.provider)
        uid, login, email = provider_api.get_identity(auth_info.token)
        if not email:
            email = provider_api.get_user_mail(auth_info.token)
        return JsonResponse({"uid": uid,
                             "login": login,
                             "email": email,
                             "provider": auth_info.provider.name.lower()})
