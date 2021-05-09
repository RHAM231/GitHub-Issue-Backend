from django.urls import path
from . import views
from . views import (
    IssueListView, IssueUpdateView, IssueCreateView, IssueView
)


# Urls for the issues app
urlpatterns = [
    path('', IssueListView.as_view(), name='issue-list'),
    path('Create/', IssueCreateView.as_view(), name='issue-create'),
    path('<slug:issue_slug>/Issue/', IssueView.as_view(), name='issue-read'),
    path('<slug:issue_slug>/Issue/Update/', IssueUpdateView.as_view(), name='issue-update'),
]