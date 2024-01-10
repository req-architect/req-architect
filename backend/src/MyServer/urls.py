# This module will map urls to app functions.
from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.seyHello),
    path("req/", views.ReqView.as_view(), name="req"),
    path("doc/", views.DocView.as_view(), name="doc"),
    path("req/link/", views.LinkView.as_view(), name="linkView"),
    path("req/unlink/", views.UnlinkView.as_view(), name="unlinkView"),
    path("login/<str:provider_str>/", views.LoginView.as_view(), name="gitlabLoginView"),
    path("login_callback/<str:provider_str>/", views.LoginCallbackView.as_view(), name="gitlabLoginCallbackView"),
    path('git/commit/', views.GitCommitView.as_view(), name="commitInRepo"),
    path("req/all/", views.AllReqsView.as_view(), name="allReqsView")
    # path('setParent/', views.setDocumentParent),
    # path('unsetParent/', views.setDocumentParentToNull)
]
