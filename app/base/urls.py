from django.urls import path
from . import views
from . views import (
    SearchResultsView
)


urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    # path('search-index', views.search_results, name='search-results'),
    path('SearchResults', SearchResultsView.as_view(), name='search-results'),
]