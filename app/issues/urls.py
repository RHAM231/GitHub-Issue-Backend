from django.urls import path
from . import views
from . views import (
    IssueListView, IssueDetailView, IssueUpdateView, IssueCreateView, IssueView
)


urlpatterns = [
    path('', IssueListView.as_view(), name='issue-list'),
    path('Create/', IssueCreateView.as_view(), name='issue-create'),
    # path('<slug:issue_slug>/', IssueDetailView.as_view(), name='issue-read'),
    path('<slug:issue_slug>/Issue/', IssueView.as_view(), name='issue-read'),
    path('<slug:issue_slug>/Issue/Update/', IssueUpdateView.as_view(), name='issue-update'),
    # path('Repositories/<int:root_id>/', RepoContentsListView.as_view(), name='project-contents'),
    # path('Repositories/Folders/<int:folder_id>/', FolderContentsListView.as_view(), name='folder-contents'),
]