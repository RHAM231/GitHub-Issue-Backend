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
        repo_slug = self.kwargs['repo_slug']
        print(repo_slug)
        repo = Repository.objects.get(slug=repo_slug)
        root_folder_name = repo.name + '_root'
        root_folder = RepoFolder.objects.get(name='repo_root', repository=repo.id, parent_folder=None)
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
        parent_folder = RepoFolder.objects.get(slug=self.kwargs['folder_slug'])
        # folder_id = self.kwargs['folder_id']
        self.folder = parent_folder

        print('PRINTED FROM FOLDER VIEW')
        count = get_issue_count(332)
        print(count)


        queryset = RepoFolder.objects.filter(parent_folder=parent_folder).annotate(issue_count=Count('repofolder'))
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
    slug_url_kwarg = 'file_slug'

    # def get_queryset(self):
    #     print('PRINTING file_id')
    #     print(self.kwargs['file_id'])
    #     queryset = RepoFile.objects.get(pk=self.kwargs['file_id'])
    #     print(queryset)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Files'
        repofile = RepoFile.objects.get(slug=self.kwargs['file_slug'])
        context['issues'] = Issue.objects.filter(associated_file=repofile.id).count
        lines = LineOfCode.objects.filter(repofile=repofile.id).annotate(issue_count=Count('issue_loc'))
        context['lines'] = lines
        context['line_count'] = lines.count()
        context['sloc'] = LineOfCode.objects.filter(repofile=repofile.id).exclude(content='').count()
        return context
