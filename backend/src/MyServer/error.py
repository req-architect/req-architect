from django.http import JsonResponse
from rest_framework import status

from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class CustomAPIException(APIException):
    api_error_code = 'CUSTOM_API_EXCEPTION'


class DoorstopException(CustomAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    api_error_code = 'Doorstop internal error'

    def __init__(self, detail='Internal Doorstop error'):
        super().__init__(detail)

class LinkCycleException(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Link cycle attempt detected.'
    api_error_code = 'LINK_CYCLE_ATTEMPT'


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(exc, CustomAPIException):
        response = JsonResponse({
            "message": response.data["detail"],
            "api_error_code": exc.api_error_code
        }, status=response.status_code)
    return response
