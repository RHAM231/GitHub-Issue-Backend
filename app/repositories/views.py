from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView
)
from . models import Repository, RepoFolder, RepoFile, LineOfCode
from issues.models import Issue
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
    template_name = 'repositories/folder_contents.html'
    context_object_name = 'folder_contents'

    def get_queryset(self):
        repo_id = self.kwargs['repo_id']
        repo = Repository.objects.get(id=repo_id)
        root_folder_name = repo.name + '_root'
        root_folder = RepoFolder.objects.get(name='repo_root', repository=repo_id, parent_folder=None)
        self.root = root_folder
        queryset = RepoFolder.objects.filter(parent_folder=root_folder.id).annotate(issue_count=Count('repofolder'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        files = RepoFile.objects.filter(parent_folder=self.root.id).annotate(issue_count=Count('repofile'))
        context['folders_and_files'] = {
            'folders': context['folder_contents'],
            'files': files
            }
        return context


def get_issue_count(parent_id):
    LineOfCode.objects.filter
    issue_count = 1
    return issue_count


class FolderContentsListView(ListView):
    model = RepoFolder
    template_name = 'repositories/folder_contents.html'
    context_object_name = 'folder_contents'

    def get_queryset(self):
        folder_id = self.kwargs['folder_id']
        self.folder = folder_id

        count = get_issue_count(332)
        print(count)


        queryset = RepoFolder.objects.filter(parent_folder=folder_id).annotate(issue_count=Count('repofolder'))
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        files = RepoFile.objects.filter(parent_folder=self.folder).annotate(issue_count=Count('repofile'))
        context['folders_and_files'] = {
            'folders': context['folder_contents'],
            'files': files
            }
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
        context['issues'] = Issue.objects.filter(associated_file=self.kwargs['file_id']).count
        lines = LineOfCode.objects.filter(repofile=self.kwargs['file_id']).annotate(issue_count=Count('issue_loc'))
        context['lines'] = lines
        context['line_count'] = lines.count()
        context['sloc'] = LineOfCode.objects.filter(repofile=self.kwargs['file_id']).exclude(content='').count()
        return context
