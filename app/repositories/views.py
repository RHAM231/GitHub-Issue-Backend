from django.shortcuts import render
from django.views.generic import (
    ListView, DeleteView, DetailView, UpdateView
)
from . models import Repository, RepoFolder, RepoFile
from django.db.models import Count


# def project_list(request):
#     context = {
#         'issue_count': 123,
#         'title': 'Projects',
#     }
#     return render(request, 'repositories/project_list.html', context)


class RepositoryListView(ListView):
    model = Repository
    template_name = 'repositories/project_list.html'
    context_object_name = 'repositories'
    queryset = Repository.objects.all().annotate(issue_count=Count('issue_repo'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['issue_count'] = self.object.issue_repo.all().count()

        return context



# def file_contents(request):
#     context = {
#         'title': 'Projects',
#         'issues_present': 3,
#     }
#     return render(request, 'base/file_contents.html', context)


# class file_contents(DetailView):
#     model = RepoFile
#     template_name = 'repositories/file_contents.html'
