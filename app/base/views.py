# Django Imports: Logic from the Django Framework
from django.shortcuts import render
from django.views.generic.edit import FormView

# Django Imports: Logic specific to this project
from issues.models import Issue
from . forms import MasterSearchForm
from . search import get_structured_search_results
from repositories.models import Repository, RepoFolder, RepoFile


##############################################################################
# BEGIN VIEWS
##############################################################################


# Renders the home page
def home(request):
    context = {
        'title': 'Home',
        # Get count data about different objects stored in the site
        'project_count': Repository.objects.all().count,
        'folder_count': RepoFolder.objects.all().count,
        'file_count': RepoFile.objects.all().count,
        'issue_count': Issue.objects.all().count,
    }
    return render(request, 'base/home.html', context)


# Search results view to return results from search field in the navbar
class SearchResultsView(FormView):
    template_name = 'base/search_results.html'
    form_class = MasterSearchForm
    success_url = 'SearchResults'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search Results'
        context['form'] = MasterSearchForm()

        form = self.form_class(self.request.GET)
        if self.request.GET and form.is_valid():
            # Call our structured method from search.py to get our
            # search results
            issues, repos, folders, files = get_structured_search_results(form)
            # Add results to context
            context['issues'] = issues
            context['repos'] = repos
            context['folders'] = folders
            context['files'] = files
        return context


# Renders the about page
def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'base/about.html', context)


##############################################################################
# END
##############################################################################
