from django.urls import path
from . import views
from . views import (
    RepositoryListView, RepoContentsListView, 
    FolderContentsListView, FileDetailView,
)


# Urls for the repositories app
urlpatterns = [
    path('', RepositoryListView.as_view(), name='project-list'),
    path('<slug:repo_slug>/Repo/', RepoContentsListView.as_view(), name='project-contents'),
    path('<slug:folder_slug>/', FolderContentsListView.as_view(), name='root-contents'),
    path('<path:folder_path>/<slug:folder_slug>/Folders/', FolderContentsListView.as_view(), name='folder-contents'),
    path('<path:file_path>/<slug:file_slug>/Files/', FileDetailView.as_view(), name='file-contents'),
]