from django.http import JsonResponse
from rest_framework import status

from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

"""
Module for handling errors that occur when working with the Doorstop API and when working with a Git module made for Python.

Each exception has a descriptive name, contains an error code and an error message. The occurrence of an exception returns an appropriate message to the client (browser).
"""


class CustomAPIException(APIException):
    api_error_code = 'CUSTOM_API_EXCEPTION'


class DoorstopException(CustomAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    api_error_code = 'DOORSTOP_INTERNAL_ERROR'

    def __init__(self, detail='Internal Doorstop error'):
        super().__init__(detail)


class PullRejectedException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    api_error_code = 'PULL_REJECTED'

    def __init__(self, detail='Pull was rejected.'):
        super().__init__(detail)


class FetchRejectedException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    api_error_code = 'FETCH_REJECTED'

    def __init__(self, detail='Fetch was rejected.'):
        super().__init__(detail)


class MergeRejectedException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    api_error_code = 'MERGE_REJECTED'

    def __init__(self, detail='Merge was rejected.'):
        super().__init__(detail)


class CloneRejectedException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    api_error_code = 'CLONE_REJECTED'

    def __init__(self, detail='Clone was rejected.'):
        super().__init__(detail)


class PushRejectedException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    api_error_code = 'PUSH_REJECTED'

    def __init__(self, detail='Push was rejected.'):
        super().__init__(detail)


class ParentOfEmptyTreeSpecifiedException(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    api_error_code = 'PARENT_OF_EMPTY_TREE_SPECIFIED'

    def __init__(self, detail='Parent document must not be specified for the document that was about to be added.'):
        super().__init__(detail)


class NoParentSpecifiedException(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    api_error_code = 'NO_PARENT_SPECIFIED'

    def __init__(self, detail='Parent document must be specified for the document that was about to be added.'):
        super().__init__(detail)


class EmptyDocumentTreeException(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    api_error_code = 'NO_DOCUMENTS'

    def __init__(self, detail='No documents were created yet.'):
        super().__init__(detail)


class InvalidReqIDException(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    api_error_code = 'INVALID_REQ_ID'

    def __init__(self, detail='Given Req ID is invalid.'):
        super().__init__(detail)


class DocNotFoundException(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    api_error_code = 'DOC_NOT_FOUND'

    def __init__(self, detail='Doc not found'):
        super().__init__(detail)


class ReqNotFoundException(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    api_error_code = 'REQ_NOT_FOUND'

    def __init__(self, detail='Req not found'):
        super().__init__(detail)


class LinkCycleException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Link cycle attempt detected.'
    api_error_code = 'LINK_CYCLE_ATTEMPT'


def custom_exception_handler(exc, context):
    """
    Function to handle a caught exception, creates an error message returned to the client.
    """
    response = exception_handler(exc, context)
    if response is not None and isinstance(exc, CustomAPIException):
        response = JsonResponse({
            "message": response.data["detail"],
            "api_error_code": exc.api_error_code
        }, status=response.status_code)
    return response
