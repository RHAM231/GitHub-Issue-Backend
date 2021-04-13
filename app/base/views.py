from django.shortcuts import render


def home(request):
    context = {
        'title': 'Home',
        'project_count': 1,
        'folder_count': 12,
        'file_count': 37,
        'issue_count': 63,
    }
    return render(request, 'base/home.html', context)


def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'base/about.html', context)