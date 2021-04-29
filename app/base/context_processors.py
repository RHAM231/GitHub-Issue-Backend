import re
import sys

from django.urls import resolve

from . path_converter import expand_path, list_to_path, path_to_namespace

from . forms import MasterSearchForm



def Master_Search_Form(request):
    form_class = MasterSearchForm
    ms_search_form = form_class()
    return {
        'ms_search_form': ms_search_form,
    }


def get_current_path(request):
    # Get our current path when we navigate to a new page and output as a list
    url_list = (request.get_full_path().split('/'))[1:-1]
    print(url_list)

    # If our path is not from Repositories or is empty (home),
    # return an empty dictionary to context to avoid breaking the site
    if not url_list:
        return {}
    elif url_list[0] != 'Repositories':
        return {}
    # Otherwise, build a dictionary of links and return it to context. We iterate over this dictionary in
    # the template to create a set of links showing the current path, where each item is a link.
    else:
        # For every item in the url_list that has an underscore, remove the underscore and everything after
        # it from the item. This will be our link names that appear on the frontend. Pass link_names to 
        # final_dict below.
        link_names = [i.replace(i, i.split('_')[0]) if '_' in i else i for i in url_list]

        # Call our expand method to get all the paths
        expanded_url_list = expand_path(url_list)

        # Call our list to path conversion method
        paths = list_to_path(expanded_url_list)

        # Call our path to namespace conversion method. This returns the
        # actual template link names used to lookup the correct path in urls.py
        namespaces = path_to_namespace(paths)

        # Pass link titles and namespaces as a dictionary to context
        final_dict = dict(zip(link_names, namespaces))

        return {
            'current_path': final_dict
        }