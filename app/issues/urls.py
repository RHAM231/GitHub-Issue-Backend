from django.urls import path
from . import views
from . views import (
    IssueListView, IssueDetailView,
)


urlpatterns = [
    path('', IssueListView.as_view(), name='issue-list'),
    path('<str:issue_slug>/', IssueDetailView.as_view(), name='issue-read'),
    # path('Repositories/<int:root_id>/', RepoContentsListView.as_view(), name='project-contents'),
    # path('Repositories/Folders/<int:folder_id>/', FolderContentsListView.as_view(), name='folder-contents'),
]