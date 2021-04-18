from django.shortcuts import render
from django.views.generic import (
    ListView, DeleteView, DetailView, UpdateView
)
from . models import Repository, RepoFolder, RepoFile, LineOfCode
from django.db.models import Count


class RepositoryListView(ListView):
    model = Repository
    template_name = 'repositories/project_list.html'
    context_object_name = 'repositories'
    queryset = Repository.objects.all().annotate(issue_count=Count('issue_repo'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['issue_count'] = self.object.issue_repo.all().count()
        context['title'] = 'Projects'
        return context


class RepoContentsListView(ListView):
    model = RepoFolder
    template_name = 'repositories/project_contents.html'
    context_object_name = 'repo_contents'

    def get_queryset(self):
        repo_id = self.kwargs['root_id']
        repo = Repository.objects.get(id=repo_id)
        root_folder_name = repo.name + '_root'
        root_folder = RepoFolder.objects.get(name='repo_root', repository=repo_id, parent_folder=None)
        self.root = root_folder
        queryset = RepoFolder.objects.all().filter(parent_folder=root_folder.id).annotate(issue_count=Count('repofolder'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        context['files'] = RepoFile.objects.all().filter(parent_folder=self.root.id).annotate(issue_count=Count('repofile'))
        return context


class FolderContentsListView(ListView):
    model = RepoFolder
    template_name = 'repositories/folder_contents.html'
    context_object_name = 'folder_contents'

    def get_queryset(self):
        folder_id = self.kwargs['folder_id']
        self.folder = folder_id
        queryset = RepoFolder.objects.all().filter(parent_folder=folder_id).annotate(issue_count=Count('repofolder'))
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        context['files'] = RepoFile.objects.all().filter(parent_folder=self.folder).annotate(issue_count=Count('repofile'))
        return context


# def file_contents(request):
#     context = {
#         'title': 'Projects',
#         'issues_present': 3,
#     }
#     return render(request, 'base/file_contents.html', context)


class FileDetailView(DetailView):
    model = RepoFile
    template_name = 'repositories/file_contents.html'
    context_object_name = 'file'
    pk_url_kwarg = 'file_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Files'
        lines = LineOfCode.objects.all().filter(repofile=self.kwargs['file_id']).annotate(issue_count=Count('issue_loc'))
        context['lines'] = lines
        context['line_count'] = lines.count()
        context['sloc'] = LineOfCode.objects.all().filter(repofile=self.kwargs['file_id']).exclude(content='').count()
        return context
