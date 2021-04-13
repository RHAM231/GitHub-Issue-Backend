from django.shortcuts import render
from repositories.models import Repository, RepoFolder, RepoFile
from issues.models import Issue


def home(request):
    context = {
        'title': 'Home',
        'project_count': Repository.objects.all().count,
        'folder_count': RepoFolder.objects.all().count,
        'file_count': RepoFile.objects.all().count,
        'issue_count': Issue.objects.all().count,
    }
    return render(request, 'base/home.html', context)


def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'base/about.html', context)