from django.shortcuts import render


def profile(request):
    context = {
        'title': 'Users',
    }
    return render(request, 'users/profile.html', context)
