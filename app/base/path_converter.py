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