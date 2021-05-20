from . forms import MasterSearchForm
from users.models import Profile
from repositories.models import Repository


def Master_Search_Form(request):
    form_class = MasterSearchForm
    ms_search_form = form_class()
    return {
        'ms_search_form': ms_search_form,
    }


def get_profile(request):
    if request.user.__class__.__name__ == "AnonymousUser":
        profile = Profile.objects.get(name='Guest')
    else:
        profile = Profile.objects.get(user=request.user)
    return {
        'profile': profile,
    }
