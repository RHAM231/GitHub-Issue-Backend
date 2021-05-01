from django.shortcuts import render
from repositories.models import Repository, RepoFolder, RepoFile
from issues.models import Issue
from . forms import MasterSearchForm
from django.views.generic.edit import FormView
from . search import get_search_results


def home(request):
    context = {
        'title': 'Home',
        'project_count': Repository.objects.all().count,
        'folder_count': RepoFolder.objects.all().count,
        'file_count': RepoFile.objects.all().count,
        'issue_count': Issue.objects.all().count,
    }
    return render(request, 'base/home.html', context)


# def search_results(request):
#     context = {
#         'title': 'Search Results'
#         }

#     return render(request, 'base/search_results.html', context)


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
            context['test'] = get_search_results(form)
            print(context['test'])

        return context


def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'base/about.html', context)