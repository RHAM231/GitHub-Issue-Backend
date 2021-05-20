from django.urls import path
from . import views


urlpatterns = [
    path('Confirm/', views.confirm_sync, name='confirm-sync'),
    path('Confirm/Success/', views.sync_success, name='sync-success'),
    path('Confirm/Failure/', views.sync_failure, name='sync-failure'),
]