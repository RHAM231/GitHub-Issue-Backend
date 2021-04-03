from consume_api.serializers import TestIssueSerializer, RepoSerializer, RepoFolderSerializer, RepoFileSerializer, IssueSerializer
from repositories.models import Repository, RepoFolder, RepoFile
from issues.models import Issue

import requests
from pprint import pprint


def get_query_url(lookup, branch=None, sha=None, path=None, issue_id=None):
    endpoint = "https://api.github.com/repos/RHAM231-IssueTracker/IssueTrackerSandbox"
    query_dict = {
        # Rate Limit
        'rate_limit': "https://api.github.com/rate_limit",
        # Repositories
        'get_repo': endpoint,
        'get_branches': endpoint + '/branches',
        'get_branch': endpoint + f'/branches/{branch}',
        # Folders
        'get_root_repo_tree': endpoint + f'/git/trees/{sha}',
        'get_folder_tree': endpoint + f'/git/trees/{sha}',
        # Files
        'get_file_contents': endpoint + f'/contents/{path}',
        # Issues
        'get_repo_issues': endpoint + '/issues',
        'create_issue': endpoint + '/issues',
        'get_issue': endpoint + f'/issues/{issue_id}',
        'update_issue': endpoint + f'/issues/{issue_id}',
        'close_issue': endpoint + f'/issues/{issue_id}',
        'open_issue': endpoint + f'/issues/{issue_id}',
    }
    url_value = query_dict.get(lookup, None)
    return url_value

repo_lookups = ['get_repo', 'get_branches', 'get_branch', 'get_root_repo_tree', 'get_folder_tree', 'get_file_contents']
issue_lookups = []


def get_serializer_and_model(slookup, raw):
    serializer_model_dict = {
        # Repositories
        'serialize_repo': (RepoSerializer(data=raw), Repository),
        'serialize_branches': 'tbd',
        'serialize_branch': 'tbd',
        # Folders
        'serialize_root_repo_tree': 'tbd',
        'serialize_folder_tree': (RepoFolderSerializer(data=raw), RepoFolder),
        # Files
        'serialize_file_contents': (RepoFileSerializer(data=raw), RepoFile),
        # Issues
        'serialize_repo_issues': (IssueSerializer(data=raw), Issue),
    }
    serializer_and_model = serializer_model_dict.get(slookup, None)
    return serializer_and_model

# 5 get functions, repo, root folder, recursive, folder, file, use json to get each next thing while dumping results in database


def get_repo(lookup):
    query_url = get_query_url(lookup)
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    serializer = RepoSerializer(data=raw)
    if serializer.is_valid():
        Repository.objects.all().delete()
        saved = serializer.save()

# fields = ['id', 'name', 'path', 'sha', 'url', 'data_type', 'mode', 'repository_url', 'parent_folder']
def get_root_folder(headers):
    # Get the GitHub project's main branch so we can access the root folder sha
    query_url_branch = get_query_url('get_branch', branch='main')
    main_branch = requests.get(query_url_branch, headers=headers)
    raw_branch = main_branch.json()
    root_folder_sha = raw_branch['commit']['commit']['tree']['sha']

    # Use the root folder sha to get the root folder
    query_url_root = get_query_url('get_root_repo_tree', sha=root_folder_sha)
    root_folder = requests.get(query_url_root, headers=headers)
    raw_folder = root_folder.json()
    y = {"repository":"1"}
    raw_folder.update(y)
    # pprint(raw_folder)

    # root_tree = raw_folder['tree']
    # folder_sha = raw_folder['sha']
    # print()
    # print('PRINTING TREE')
    # print()
    # pprint(root_tree)
    # print()

    # For testing/development purposes, let's flush our model before we save the folder
    RepoFolder.objects.all().delete()
    RepoFile.objects.all().delete()

    # Now save it to our database using DRF serializer
    serializer = RepoFolderSerializer(data=raw_folder)
    # print(serializer)
    if serializer.is_valid():
        saved = serializer.save(name='repo_root', path='tbd', data_type='tree', mode='040000', parent_folder=None)
        # print('PRINTING SAVED')
        # print(saved)
    
    # Call our recursive method
    unpack_repository(raw_folder, headers)


def unpack_repository(folder, headers):
    tree = folder['tree']
    folder_sha = folder['sha']
    print()
    print('PRINTING UPACKING RESULTS')
    for entry in tree:
        if entry['type'] == 'blob':
            print('blob')
            get_repofile(entry, headers, folder_sha)
        elif entry['type'] == 'tree':
            print('tree')
            get_repofolder(entry, headers, folder_sha)


def get_repofolder(folder_listing, headers, folder_sha):
    current_sha = folder_listing['sha']
    query_url = get_query_url('get_folder_tree', sha=current_sha)

    # print()
    # print('PRINTING QUERY URL FOR FOLDER')
    # print(query_url)
    # print()

    r = requests.get(query_url, headers=headers)
    raw_subfolder = r.json()

    # print()
    # print('PRINTING FOLDER LISTING')
    # print(folder_listing)
    # print()

    # print()
    # print('PRINTING RAW SUBFOLDER')
    # pprint(raw_subfolder)
    # print()

    serialize_github_object('serialize_folder_tree', raw_subfolder, folder_listing=folder_listing, folder_sha=folder_sha)

    # serializer = RepoSerializer(data=raw)
    # if serializer.is_valid():
    #     Repository.objects.all().delete()
    #     saved = serializer.save()


def get_repofile(file_listing, headers, folder_sha):
    # print()
    # print('PRINTING FILE LISTING')
    # print(file_listing)
    path = file_listing['path']
    # print(path)
    # print()
    query_url = get_query_url('get_file_contents', path=path)
    # print('PRINTING QURL')
    # print(query_url)
    # print()
    r = requests.get(query_url, headers=headers)
    raw_file = r.json()
    # pprint(raw_file)
    serialize_github_object('serialize_file_contents', raw_file, file_listing=file_listing, folder_sha=folder_sha)
    # serializer = RepoSerializer(data=raw_file)
    # if serializer.is_valid():
    #     Repository.objects.all().delete()
    #     saved = serializer.save()


def serialize_github_object(slookup, raw, file_listing=None, folder_listing=None, folder_sha=None):
    # print()
    # print('PRINTING RAW')
    # pprint(raw)
    # print()
    # print('PRINTING FILE LISTING')
    # print(file_listing)

    parent_folder = RepoFolder.objects.get(sha=folder_sha).pk
    parent_folder_pk = str(parent_folder)
    injected_json = {"repository":"1", "repofolder":parent_folder_pk}
    raw.update(injected_json)

    # print()
    # print('PRINTING UPDATED RAW')
    # pprint(raw)
    # print()

    serializer, model = get_serializer_and_model(slookup, raw)
    # print(serializer)
    # print(model)

    if serializer.is_valid():
        if file_listing:
            saved = serializer.save(data_type=file_listing['type'])
        elif folder_listing:
            print()
            print('PRINTING FOLDER LISTING FROM WITHIN SERIALIZER METHOD')
            print(folder_listing)
            print()
            name=folder_listing['path']
            path='tbd'
            data_type=folder_listing['type']
            mode=folder_listing['mode']
            saved = serializer.save(name=name, path=path, data_type=data_type, mode=mode)
        else:
            saved = serializer.save()
