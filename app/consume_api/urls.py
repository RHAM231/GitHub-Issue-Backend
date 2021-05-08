from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from consume_api import views


# Define our urls for our REST portion that interfaces with GitHub
urlpatterns = [
    # API Home
    path('', views.api_root, name='api-home'),
    # Issues
    path('Issues-List/', views.IssueList.as_view(), name='api-issue-list'),
    path('Issues-List/<int:pk>/', views.IssueDetail.as_view()),
    # Repositories
    path('Repositories-List/', views.RepoList.as_view(), name='api-repo-list'),
    path('Repositories-List/<int:pk>/', views.RepoDetail.as_view()),
    # Folders
    path('Folders-List/', views.RepoFolderList.as_view(), name='api-folder-list'),
    path('Folders-List/<int:pk>/', views.RepoFolderDetail.as_view()),
    # Files
    path('Files-List/', views.RepoFileList.as_view(), name='api-file-list'),
    path('Files-List/<int:pk>/', views.RepoFileDetail.as_view()),
    # Test
    path('issues_test/', views.TestIssueList.as_view()),
    path('issues_test/<int:pk>/', views.TestIssueDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)