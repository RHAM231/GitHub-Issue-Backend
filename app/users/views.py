from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Profile
# from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# @login_required
def profile(request):
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST,
    #                                request.FILES,
    #                                instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('profile')

    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)

    if request.user.__class__.__name__ == "AnonymousUser":
        profile = Profile.objects.get(name='Guest')
    else:
        profile = Profile.objects.get(user=request.user)

    context = {
        # 'u_form': u_form,
        # 'p_form': p_form,
        'title': 'Users',
        'profile': profile
    }

    return render(request, 'users/profile.html', context)
