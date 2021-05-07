from . forms import MasterSearchForm
from users.models import Profile


# Adds our navbar search form to context so we can access it from every page
def Master_Search_Form(request):
    form_class = MasterSearchForm
    ms_search_form = form_class()
    return {
        'ms_search_form': ms_search_form,
    }


# Adds our user to context for the entire site to avoid loading it multiple times in multiple views
def get_profile(request):
    if request.user.__class__.__name__ == "AnonymousUser":
        profile = Profile.objects.get(name='Guest')
    else:
        profile = Profile.objects.get(user=request.user)
    return {
        'profile': profile,
    }
