from django.shortcuts import render


# Create a simple profile detail view for guests
# The url is in GITB.urls.py
def profile(request):
    context = {
        'title': 'Users',
    }
    return render(request, 'users/profile.html', context)
