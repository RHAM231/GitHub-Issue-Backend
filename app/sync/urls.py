from django.urls import path
from . import views


urlpatterns = [
    path('Confirm/', views.confirm_sync, name='confirm-sync'),
    path('Success', views.sync_success, name='sync-success'),
]