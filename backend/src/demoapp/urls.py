# This module will map urls to app functions.
from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.sey_hello)
]