# Django Imports: Logic from the Django Framework
from django.conf import settings
from django.shortcuts import render

# Django Imports: Logic specific to this project
from . github_client import get_repo
from repositories.models import Repository
from users.models import Profile


# Define a view to begin the GitHub repo import process
def confirm_sync(request):
    if request.method == 'POST':
        token = settings.TEST_TOKEN
        headers = {
            'Authorization': f'token {token}',
            }
        user = request.user
        get_repo('get_repo', headers, user)
        # Use AJAX to redirect after successful form submission

    return render(request, 'sync/confirm_sync.html')


# Define a view to display a success message after importing a GitHub repo
def sync_success(request):
    return render(request, 'sync/sync_success.html')
