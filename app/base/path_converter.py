from django.urls import resolve

# Given a single path, get a list of lists of all paths contained in our single path
def expand_path(url_list):
    i=1
    expanded_url_list=[]
    while i <=len(url_list):
        expanded_url_list.append(url_list[0:i])
        i+=1
    return expanded_url_list


# Given lists containing each path item as a list item, join these together with '/'s to get real paths.
# For foreign key parameters, do some additional formatting to capture the extra parameters.
def list_to_path(expanded_url_list):
    paths=[]
    for expanded_url in expanded_url_list:
        joined_url = '/'.join(expanded_url)
        underscore_present = [i for i in expanded_url if '_' in i]
        if underscore_present:
            test_string = underscore_present[0]
            underscore_present = test_string.split('_')[0]
            joined_url = joined_url.replace(test_string, underscore_present)
            path_w_fk_lookup = []
            path_w_fk_lookup.append(joined_url)
            slug_parameter = [test_string for path_string in expanded_url if '_' in path_string]
            paths.append(path_w_fk_lookup + slug_parameter)
        else:
            paths.append(joined_url)
    return paths


def path_to_namespace(paths):
    namespaces = []
    for path in paths:
        if isinstance(path, list):
            path[0] = '/' + path[0] + '/'
            path[0] = resolve(path[0]).url_name
        else:
            path = '/' + path + '/'
            path = resolve(path).url_name
            namespaces.append(path)
        return namespaces