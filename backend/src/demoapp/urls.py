# This module will map urls to app functions.
from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.sey_hello),
    path('docs/', views.getDocuments),
    path('reqs/', views.getReqs),
    path('addDoc/', views.add_Document),
    path('addreq/', views.add_Requirement),
    path('delDoc/', views.delete_Document),
    path('delReq/', views.delete_Requirement),
    path('editReq/', views.edit_Requirement),
    path('linkReqs/', views.link_Requirements),
    path('unlinkReqs/', views.unlink_Requirements)
]
