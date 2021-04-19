from django.urls import path
from . import views
from . views import (
    RepositoryListView, RepoContentsListView, 
    FolderContentsListView, FileDetailView,
)


urlpatterns = [
    # path('confirm-sync', views.confirm_sync, name='confirm-sync'),
    # path('sync-success', views.sync_success, name='sync-success'),
    path('', RepositoryListView.as_view(), name='project-list'),
    path('test/<int:repo_id>/', RepoContentsListView.as_view(), name='project-contents'),
    path('Folders/<int:folder_id>/', FolderContentsListView.as_view(), name='folder-contents'),
    path('Folders/Files/<int:file_id>/', FileDetailView.as_view(), name='file-contents'),
]