from django.urls import path
from . import views
from . views import (
    IssueListView, IssueUpdateView, IssueCreateView, IssueView, load_files
)


# Urls for the issues app
urlpatterns = [
    path('', IssueListView.as_view(), name='issue-list'),
    path('Create/', IssueCreateView.as_view(), name='issue-create'),
    path('ajax/load_files/', views.load_files, name='ajax_load_files'),
    path('<slug:issue_slug>/Issue/', IssueView.as_view(), name='issue-read'),
    path('<slug:issue_slug>/Issue/Update/', IssueUpdateView.as_view(), name='issue-update'),
]