from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from consume_api import views


urlpatterns = [
    path('issues_test/', views.IssueList.as_view()),
    path('issues_test/<int:pk>/', views.IssueDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)