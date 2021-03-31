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
        'get_repo': (RepoSerializer(data=raw), Repository),
        'get_branches': 'tbd',
        'get_branch': 'tbd',
        # Folders
        'get_root_repo_tree': 'tbd',
        'get_folder_tree': (RepoFolderSerializer(data=raw), RepoFolder),
        # Files
        'get_file_contents': (RepoFileSerializer(data=raw), RepoFile),
        # Issues
        'get_repo_issues': (IssueSerializer(data=raw), Issue),
    }
    serializer_and_model = serializer_model_dict.get(slookup, None)
    return serializer_and_model

# 4 get functions, repo, root folder, folder, file, use json to get each next thing while dumping results in database


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
    pprint(raw_folder)

    # Now save it to our database using DRFs
    serializer = RepoFolderSerializer(data=raw_folder)
    print(serializer)
    if serializer.is_valid():
        print('boo')
        # For testing/development purposes, let's flush our model before we save the folder
        RepoFolder.objects.all().delete()
        saved = serializer.save(name='repo_root', path='tbd', data_type='tree', mode='040000', parent_folder=None)
        print('PRINTING SAVED')
        print(saved)


def get_repofolder(lookup):
    query_url = get_query_url(lookup)
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    serializer = RepoSerializer(data=raw)
    if serializer.is_valid():
        Repository.objects.all().delete()
        saved = serializer.save()


def get_repofile(lookup):
    query_url = get_query_url(lookup)
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    serializer = RepoSerializer(data=raw)
    if serializer.is_valid():
        Repository.objects.all().delete()
        saved = serializer.save()


def serialize_github_object(slookup, raw):
    # query_url = get_query_url(lookup)
    # r = requests.get(query_url, headers=headers)
    # raw = r.json()

    serializer, model = get_serializer_and_model(slookup, raw)
    if serializer.is_valid():
        model.objects.all().delete()
        saved = serializer.save()
