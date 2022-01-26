# Django Imports: Logic from the Django Framework
from django.db.models import Count
from django.shortcuts import render

# Django Imports: Generic Views
from django.views.generic import (
    ListView, DetailView
)

# Django Imports: Logic specific to this project
from issues.models import Issue
from . models import Repository, RepoFolder, RepoFile, LineOfCode


##############################################################################
# SUMMARY
##############################################################################

'''
Let's define views to display a GitHub repo file structure. We use
Django's generic ListView for the repos and folders, and DetailView for
individual files. We'll override the views' get_queryset() and
get_context_data() methods to customize our display data.
'''

##############################################################################
# BEGIN VIEWS
##############################################################################


# List all the GitHub repositories that have been imported to the site
class RepositoryListView(ListView):
    model = Repository
    template_name = 'repositories/project_list.html'
    context_object_name = 'repositories'
    # Define our queryset. Annotate it with all its fk related issues
    queryset = Repository.objects.all().annotate(
        issue_count=Count('issue_repo'))

    # Override get_context_data() to set the page title
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Repositories'
        return context


# List all the folders and files in the repository root folder
class RepoContentsListView(ListView):
    model = RepoFolder
    template_name = 'repositories/folder_contents.html'
    context_object_name = 'folder_contents'

    # Override get_queryset() to define a folder list by the given
    # repo_slug from the url
    def get_queryset(self):
        # Get our slug from kwargs (url), use it to get our repo
        repo_slug = self.kwargs['repo_slug']
        repo = Repository.objects.get(slug=repo_slug)

        # Use our repo to get our root folder
        root_folder_name = repo.name + '_root'
        root_folder = RepoFolder.objects.get(
            name='repo_root', 
            repository=repo.id, 
            parent_folder=None
            )
        # Save root so we can access it in get_context_data() to list
        # our files
        self.root = root_folder

        # Now get all the folders in root and annotate them with their
        # associated issue counts
        queryset = RepoFolder.objects.filter(
            parent_folder=root_folder.id).annotate(
                issue_count=Count('repofolder'))
        return queryset

    # Override get_context_data() to add items to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Repositories'

        # Get a list of all files in the root folder by using self.root
        # from get_queryset(). Add the issues count.
        files = RepoFile.objects.filter(
            parent_folder=self.root).annotate(issue_count=Count('repofile'))
        # Grab our folder_contents queryset defined by get_queryset()
        # and add it to context with files as a dictionary. This allows
        # us to minimize our html by iterating over one context object
        # rather than two
        context['folders_and_files'] = {
            'folders': context['folder_contents'],
            'files': files
            }
        return context


# List all the contents of a regular folder
class FolderContentsListView(ListView):
    model = RepoFolder
    template_name = 'repositories/folder_contents.html'
    context_object_name = 'folder_contents'

    # Override get_queryset() to list folders by parent folder
    def get_queryset(self):
        # Get the parent folder using the slug from the url
        parent_folder = RepoFolder.objects.get(
            slug=self.kwargs['folder_slug']
            )
        self.folder = parent_folder
        # Define the folder queryset by the parent folder. Annotate
        # each folder with its issue count
        queryset = RepoFolder.objects.filter(
            parent_folder=parent_folder).annotate(
                issue_count=Count('repofolder'))
        return queryset

    # Override get_context_data() to combine our files and folders into
    # a single queryset.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Repositories'

        # Get a list of all our files in the given folder
        files = RepoFile.objects.filter(
            parent_folder=self.folder).annotate(
                issue_count=Count('repofile'))

        # Grab our folder_contents queryset defined by get_queryset()
        # and add it to context with files as a dictionary. This allows
        # us to minimize our html by iterating over one context object
        # rather than two
        context['folders_and_files'] = {
            'folders': context['folder_contents'],
            'files': files
            }
        return context


# Display a single file with all its attributes and lines of code
class FileDetailView(DetailView):
    model = RepoFile
    template_name = 'repositories/file_contents.html'
    context_object_name = 'file'
    slug_url_kwarg = 'file_slug'

    # Override get_context_data()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Files'

        # Get our file from our url slug
        repofile = RepoFile.objects.get(slug=self.kwargs['file_slug'])

        # Get our issues associated to the given file
        context['issues'] = Issue.objects.filter(
            associated_file=repofile.id).count

        # Get our lines of code to iterate over in the template
        lines = LineOfCode.objects.filter(
            repofile=repofile.id).order_by(
                'line_number').annotate(
                    issue_count=Count('issue_loc'))

        # Define our individual file attributes
        context['lines'] = lines
        context['line_count'] = lines.count()
        context['sloc'] = LineOfCode.objects.filter(
            repofile=repofile.id).exclude(content='').count()
        return context


##############################################################################
# END
##############################################################################
