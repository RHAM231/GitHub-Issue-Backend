# Django Imports: Logic from the Django Framework
from django.conf import settings
from django.shortcuts import render

# Django Imports: Logic specific to this project
from users.models import Profile
from . forms import ImportRepoForm
from . github_client import get_repo
from repositories.models import Repository



# Define a view to begin the GitHub repo import process
def confirm_sync(request):
    # If a form submission took place
    if request.method == 'POST':
        # Call our import form with post data
        form = ImportRepoForm(request.POST)
        if form.is_valid():
            # Get our repo choice
            repo_name = form.cleaned_data['repository']

            # Get our authentication data to pass to our github_client script
            token = settings.TEST_TOKEN
            headers = {'Authorization': f'token {token}',}
            user = request.user

            # Call our get_repo method in github_client.py to begin the import process
            get_repo('get_repo', repo_name, headers, user)
            # While we wait, use AJAX to display a spinner and load message
            # Use AJAX to redirect after successful form submission
    
    # Otherwise we've loaded the page for the first time, display an
    # empty form
    else:
        form = ImportRepoForm()
    
    # Pass form to context
    context = {'form': form}

    # Render the page with the empty form
    return render(request, 'sync/confirm_sync.html', context)


# Define a view to display a success message after importing a GitHub repo
def sync_success(request):
    return render(request, 'sync/sync_success.html')


# Define a view to display a failure message after importing a GitHub repo
def sync_failure(request):
    return render(request, 'sync/sync_failure.html')
