from django.urls import resolve
from django.template.defaultfilters import slugify
from repositories import models

# Given a single path, get a list of lists of all paths contained in our single path
def expand_path(url_list):
    i=1
    expanded_url_list=[]
    while i <=len(url_list):
        expanded_url_list.append(url_list[0:i])
        i+=1
    if expanded_url_list[-1][-1] in ('Folders', 'Files'):
        expanded_url_list.remove(expanded_url_list[-2])

    url_pairs = []
    url_pairs.append(('First', expanded_url_list[0]))
    if len(expanded_url_list) > 1:
        for entry in expanded_url_list[1:]:
            if 'Folders' in entry:
                entry = ('Folder', entry)
            elif 'Files' in entry:
                entry = ('File', entry)
            elif entry == expanded_url_list[1]:
                entry = ('Repository', entry)
            url_pairs.append(entry)
    print('PRINTING URL PAIRS')
    print(url_pairs)
    print()

    # expanded_url_list[0] = (('First', expanded_url_list[0]))
    # for entry in expanded_url_list[0:]:
    #     if 'Folders' in entry:
    #         expanded_url_list[entry] = ('Folder', entry)
    #     elif 'Files' in entry:
    #         expanded_url_list[entry] = ('File', entry)
    #     elif entry == expanded_url_list[1]:
    #         expanded_url_list[entry] = ('Repository', entry)
    # print('PRINTING Expanded with replace')
    # print(expanded_url_list)
    # print()

    url_dict = {}
    url_dict['First'] = expanded_url_list[0]
    if len(expanded_url_list) > 1:
        for entry in expanded_url_list[0:]:
            if 'Folders' in entry:
                url_dict['Folder'] = entry
            elif 'Files' in entry:
                url_dict['File'] = entry
            elif entry == expanded_url_list[1]:
                url_dict['Repository'] = entry
    print('PRINTING URL DICT')
    print(url_dict)
    print()
    # return expanded_url_list
    return url_dict


# Given lists containing each path item as a list item, join these together with '/'s to get real paths.
# For foreign key parameters, do some additional formatting to capture the extra parameters.
def list_to_path(url_dict):
    paths=[]
    print('STARTING TO BUILD PATHS ...')
    for key, expanded_url in url_dict.items():
        print('expanded, joined')
        print(expanded_url)
        joined_url = '/'.join(expanded_url)
        underscore_present = [i for i in expanded_url if '_' in i]

        print(joined_url)
        print()

        if key == 'First':
            paths.append(joined_url)

        else:
            if key == 'Repository':
                try:
                    slug_parameter = models.Repository.objects.get(name=expanded_url[1]).slug
                except models.Repository.DoesNotExist:
                    slug_parameter = models.Repository.objects.get(slug=expanded_url[-1]).slug

            elif key == 'Folder':
                try:
                    slug_parameter = models.RepoFolder.objects.get(issuetracker_url_path=joined_url).slug
                except models.RepoFolder.DoesNotExist:
                    slug_parameter = models.RepoFolder.objects.get(slug=expanded_url[-2]).slug

            elif key == 'File':
                try:
                    slug_parameter = models.RepoFile.objects.get(issuetracker_url_path=joined_url).slug
                except models.RepoFile.DoesNotExist:
                    slug_parameter = models.RepoFile.objects.get(slug=expanded_url[-2]).slug


            paths.append([joined_url, slug_parameter])
        print('current path iteration')
        print(paths)
        print()


        # if underscore_present:
        #     test_string = underscore_present[0]
        #     underscore_present = test_string.split('_')[0]
        #     joined_url = joined_url.replace(test_string, underscore_present)
        #     path_w_fk_lookup = []
        #     path_w_fk_lookup.append(joined_url)
        #     slug_parameter = [test_string for path_string in expanded_url if '_' in path_string]
        #     paths.append(path_w_fk_lookup + slug_parameter)
        # elif len(expanded_url) > 1:
        #     if expanded_url == expanded_url_list[1]:
        #         print(joined_url)
        #         slug_parameter = models.Repository.objects.get(name=expanded_url[1]).slug
        #         print('PRINTING SLUG')
        #         print(slug_parameter)
        #         paths.append([joined_url, slug_parameter])
        # else:
        #     paths.append(joined_url)



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