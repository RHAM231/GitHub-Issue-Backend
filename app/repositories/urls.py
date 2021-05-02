from django.urls import path, register_converter
from . import converters, views
from . views import (
    RepositoryListView, RepoContentsListView, 
    FolderContentsListView, FileDetailView,
)

register_converter(converters.CustomPathConverter, 'cpath')

urlpatterns = [
    # path('confirm-sync', views.confirm_sync, name='confirm-sync'),
    # path('sync-success', views.sync_success, name='sync-success'),
    path('', RepositoryListView.as_view(), name='project-list'),
    path('<slug:repo_slug>/Repo', RepoContentsListView.as_view(), name='project-contents'),
    path('<slug:folder_slug>/Root', FolderContentsListView.as_view(), name='root-contents'),
    # path('Repository/<path:file_path>/<int:file_id>/', FileDetailView.as_view(), name='file-contents'),
    path('<path:folder_path>/<slug:folder_slug>/Folders/', FolderContentsListView.as_view(), name='folder-contents'),
    path('<path:file_path>/<slug:file_slug>/Files/', FileDetailView.as_view(), name='file-contents'),
]