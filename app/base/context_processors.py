from . forms import MasterSearchForm


# 
def Master_Search_Form(request):
    form_class = MasterSearchForm
    ms_search_form = form_class()
    return {
        'ms_search_form': ms_search_form,
    }
