from django.http import HttpResponse

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


def sey_hello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    return HttpResponse('Hello from backend')
