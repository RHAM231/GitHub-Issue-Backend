from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from consume_api import views


urlpatterns = [
    # Issues
    path('issues_real/', views.IssueList.as_view()),
    path('issues_real/<int:pk>/', views.IssueDetail.as_view()),
    # Repositories
    path('repositories/', views.RepoList.as_view()),
    path('repositories/<int:pk>/', views.RepoDetail.as_view()),
    # Folders
    path('folders/', views.RepoFolderList.as_view()),
    path('folders/<int:pk>/', views.RepoFolderDetail.as_view()),
    # Files
    path('files/', views.RepoFileList.as_view()),
    path('files/<int:pk>/', views.RepoFileDetail.as_view()),
    # Test
    path('issues_test/', views.TestIssueList.as_view()),
    path('issues_test/<int:pk>/', views.TestIssueDetail.as_view()),
    # path('', views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)