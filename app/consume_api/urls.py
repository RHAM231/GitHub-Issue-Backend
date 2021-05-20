from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from consume_api import views


urlpatterns = [
    path('', views.api_root, name='api-home'),
    path('Issues-List/', views.IssueList.as_view(), name='api-issue-list'),
    path('Issues-List/<int:pk>/', views.IssueDetail.as_view(), name='api-issue-detail'),
    path('Repositories-List/', views.RepoList.as_view(), name='api-repo-list'),
    path('Repositories-List/<int:pk>/', views.RepoDetail.as_view(), name='api-repo-detail'),
    path('Folders-List/', views.RepoFolderList.as_view(), name='api-folder-list'),
    path('Folders-List/<int:pk>/', views.RepoFolderDetail.as_view(), name='api-folder-detail'),
    path('Files-List/', views.RepoFileList.as_view(), name='api-file-list'),
    path('Files-List/<int:pk>/', views.RepoFileDetail.as_view(), name='api-file-detail'),
    path('issues_test/', views.TestIssueList.as_view()),
    path('issues_test/<int:pk>/', views.TestIssueDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)