from django.http import HttpResponse
from demoapp.models import Example

# Create your views here.
# Views - they are really request handlers, byt Django has weird naming style


def sey_hello(request) -> HttpResponse:
    """A simple hello world function to check if connection between the app and the server is correctly established"""
    b = Example.objects.get(pk=1)
    return HttpResponse(f'Name of example of id=1: {b.name}')
