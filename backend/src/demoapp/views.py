from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import demoapp.restHandlersHelpers
import doorstop

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


def sey_hello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')


@api_view(["POST"])
def add_Document(request):
    pass


@api_view(["POST"])
def add_Requirement(request):
    pass


@api_view(["POST"])
def delete_Document(request):
    pass


@api_view(["POST"])
def delete_Requirement(request):
    pass


@api_view(["GET"])
def getDocuments(request):
    if request.method == "GET":
        try:
            documents = demoapp.restHandlersHelpers.getDocuments()
            serialized = demoapp.restHandlersHelpers.serializeDocuments(
                documents)
            return JsonResponse(serialized, safe=False)
        except doorstop.DoorstopError:
            return JsonResponse([], safe=False)
    else:
        return Response({'message': 'Unsupported request method'}, status=status.HTTP_400_BAD_REQUEST)
