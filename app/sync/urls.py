from django.urls import path
from . import views


urlpatterns = [
    path('confirm-sync', views.confirm_sync, name='confirm-sync'),
    # path('sync-success', views.sync_success, name='sync-success'),
]