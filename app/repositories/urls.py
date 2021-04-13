from django.urls import path
from . import views
from . views import (
    RepositoryListView
)


urlpatterns = [
    # path('confirm-sync', views.confirm_sync, name='confirm-sync'),
    # path('sync-success', views.sync_success, name='sync-success'),
    path('Repositories', RepositoryListView.as_view(), name='project-list'),
]