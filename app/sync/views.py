from django.conf import settings
from django.shortcuts import render
from users.models import Profile
from . forms import ImportRepoForm
from . github_client import get_repo
from repositories.models import Repository
from csp.decorators import csp_exempt


@csp_exempt
def confirm_sync(request):
    if request.method == 'POST':
        form = ImportRepoForm(request.POST)
        if form.is_valid():
            repo_name = form.cleaned_data['repository']
            token = settings.GH_TOKEN
            headers = {'Authorization': f'token {token}',}
            user = request.user
            get_repo('get_repo', repo_name, headers, user)
    else:
        form = ImportRepoForm()
    context = {'form': form}
    return render(request, 'sync/confirm_sync.html', context)


def sync_success(request):
    return render(request, 'sync/sync_success.html')


def sync_failure(request):
    return render(request, 'sync/sync_failure.html')
