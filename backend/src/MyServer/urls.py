# This module will map urls to app functions.
from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.seyHello),
    path("req/", views.ReqView.as_view(), name="req"),
    path("doc/", views.DocView.as_view(), name="doc")
    # path('setParent/', views.setDocumentParent),
    # path('unsetParent/', views.setDocumentParentToNull)
]