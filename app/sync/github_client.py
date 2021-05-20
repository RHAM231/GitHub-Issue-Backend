import os
import base64
import requests
from pprint import pprint
from github import Github, GithubException
from issues.models import Issue
from users.models import Profile
from repositories.models import Repository, RepoFolder, RepoFile, LineOfCode
from consume_api.serializers import RepoSerializer, RepoFolderSerializer, RepoFileSerializer, IssueSerializer


def get_query_url(lookup, repo, branch=None, sha=None, path=None, issue_id=None):
    if repo == 'IssueTrackerSandbox':
        endpoint = "https://api.github.com/repos/RHAM231-IssueTracker/IssueTrackerSandbox"
    elif repo == 'Sandbox-Import':
        endpoint = "https://api.github.com/repos/RHAM231-IssueTracker/Sandbox-Import"
    
    query_dict = {
        'rate_limit': "https://api.github.com/rate_limit",
        'get_repo': endpoint,
        'get_branches': endpoint + '/branches',
        'get_branch': endpoint + f'/branches/{branch}',
        'get_root_repo_tree': endpoint + f'/git/trees/{sha}',
        'get_folder_tree': endpoint + f'/git/trees/{sha}',
        'get_file_contents': endpoint + f'/contents/{path}',
        'get_repo_issues': endpoint + '/issues',
        'create_issue': endpoint + '/issues',
        'get_issue': endpoint + f'/issues/{issue_id}',
        'update_issue': endpoint + f'/issues/{issue_id}',
    }
    url_value = query_dict.get(lookup, None)
    return url_value


def get_serializer_and_model(slookup, raw):
    serializer_model_dict = {
        'serialize_repo': (RepoSerializer(data=raw), Repository),
        'serialize_folder_tree': (RepoFolderSerializer(data=raw), RepoFolder),
        'serialize_file_contents': (RepoFileSerializer(data=raw), RepoFile),
        'serialize_repo_issue': (IssueSerializer(data=raw), Issue),
    }
    serializer_and_model = serializer_model_dict.get(slookup, None)
    return serializer_and_model


def get_repo(lookup, repo_name, headers, user):
    query_url = get_query_url(lookup, repo_name)
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    repo_url = raw['url']
    repo_branch = raw['default_branch']

    Repository.objects.filter(name=repo_name).delete()

    serializer = RepoSerializer(data=raw)
    if serializer.is_valid():
        serializer.save()
    
    repo_pk = str(Repository.objects.get(url=repo_url).pk)

    get_root_folder(repo_pk, repo_name, repo_branch, headers)
    get_repo_issues('get_repo_issues', repo_name, repo_pk, headers, user)


def get_root_folder(repo_pk, repo_name, repo_branch, headers):
    query_url_branch = get_query_url('get_branch', repo_name, branch=repo_branch)
    main_branch = requests.get(query_url_branch, headers=headers)
    raw_branch = main_branch.json()
    root_folder_sha = raw_branch['commit']['commit']['tree']['sha']

    query_url_root = get_query_url('get_root_repo_tree', repo_name, sha=root_folder_sha)
    root_folder = requests.get(query_url_root, headers=headers)
    raw_folder = root_folder.json()
    injected_json = {"repository":repo_pk, "parent_folder":None}
    raw_folder.update(injected_json)

    serializer = RepoFolderSerializer(data=raw_folder)
    if serializer.is_valid():
        saved = serializer.save(name='repo_root', path='', data_type='tree', mode='040000')
    
    unpack_repository(repo_pk, repo_name, raw_folder, headers, '')

 
def unpack_repository(repo_pk, repo_name, folder, headers, current_path):
    tree = folder['tree']
    folder_sha = folder['sha']
    for entry in tree:
        if entry['type'] == 'blob':
            get_repofile(repo_pk, repo_name, entry, headers, folder_sha, current_path)
        elif entry['type'] == 'tree':
            get_repofolder(repo_pk, repo_name, entry, headers, folder_sha, current_path)


def get_repofolder(repo_pk, repo_name, folder_listing, headers, folder_sha, current_path):
    current_sha = folder_listing['sha']
    query_url = get_query_url('get_folder_tree', repo_name, sha=current_sha)

    r = requests.get(query_url, headers=headers)
    raw_subfolder = r.json()

    serialize_github_object(
        repo_pk, 'serialize_folder_tree', raw_subfolder, path=current_path,
        folder_listing=folder_listing, folder_sha=folder_sha
        )

    if current_path == '':
        current_path = current_path + folder_listing['path']
    else:
        current_path = current_path + '/' + folder_listing['path']
    unpack_repository(repo_pk, repo_name, raw_subfolder, headers, current_path)


def get_repofile(repo_pk, repo_name, file_listing, headers, folder_sha, current_path):
    if current_path == '':
        path = current_path + file_listing['path']
    else:
        path = current_path + '/' + file_listing['path']

    query_url = get_query_url('get_file_contents', repo_name, path=path)
    
    r = requests.get(query_url, headers=headers)
    raw_file = r.json()

    serialize_github_object(
        repo_pk, 'serialize_file_contents', raw_file, 
        file_listing=file_listing, folder_sha=folder_sha
        )
    
    file_content = raw_file['content']
    file_sha = raw_file['sha']
    file_path = raw_file['path']
    parent_file = RepoFile.objects.get(sha=file_sha, path=file_path)
    save_locs(file_content, parent_file)
    

def save_locs(content, parent_file):
    decoded = base64.b64decode(content)
    lines_of_code = [item.decode('utf-8') for item in decoded.splitlines()]

    for i, line in enumerate(lines_of_code):
        new_line = LineOfCode(content=line, line_number=i, repofile=parent_file)
        new_line.save()


def get_repo_issues(lookup, repo_name, repo_pk, headers, user):
    query_url = get_query_url(lookup, repo_name)
    r = requests.get(query_url, headers=headers)
    raw_issues_list = r.json()
    issue_numbers = [issue['number'] for issue in raw_issues_list]
    issue_numbers.reverse()
    for number in issue_numbers:
        get_issue('get_issue', repo_pk, repo_name, headers, number, user)


def check_for_stamp(body):
    if body:
        nlines = body.count('\n')
        if nlines >= 5:
            line5 = body.splitlines()[4]
            line6 = body.splitlines()[5]
            if 'Generated by Issue Tracker: ' in line5 and 'Stamp Id: ' in line6:
                check_results = True
            else:
                check_results = False
        else:
            check_results = False
    else:
        check_results = False
    return check_results


def extract_stamp_data(body):
    path = (body.splitlines()[0]).replace('Issue Location: ', '')
    folder = (body.splitlines()[1]).replace('Affected Folder: ', '')
    file = (body.splitlines()[2]).replace('Affected File: ', '')
    loc = (body.splitlines()[3]).replace('Affected Line of Code: ', '')

    if loc != 'None':
        path_and_file = path.rsplit('/', 1)
        file_id = RepoFile.objects.get(issuetracker_url_path=path_and_file[0], name=path_and_file[1])
        loc = LineOfCode.objects.get(path=path_and_file[0], line_number=loc, repofile=file_id)
        loc_pk = str(loc.pk)
        injected_json = {"associated_loc":loc_pk, "associated_file":None, "associated_folder":None}

    elif file != 'None':
        path_and_file = path.rsplit('/', 1)
        file = RepoFile.objects.get(issuetracker_url_path=path_and_file[0], name=path_and_file[1])
        file_pk = str(file.pk)
        injected_json = {"associated_loc":None, "associated_file":file_pk, "associated_folder":None}

    else:
        folder = RepoFolder.objects.get(issuetracker_url_path=path, name=folder)
        folder_pk = str(folder.pk)
        injected_json = {"associated_loc":None, "associated_file":None, "associated_folder":folder_pk}

    return injected_json


def remove_stamp(body):
    nlines = body.count('\n')
    if nlines == 5:
        body = ''
    else:
        body = body.split('\n',7)[7]
    return body


def get_issue(lookup, repo_pk, repo_name, headers, issue_id, user):
    query_url = get_query_url(lookup, repo_name, issue_id=issue_id)
    r = requests.get(query_url, headers=headers)
    raw_issue = r.json()

    stamp_present = check_for_stamp(raw_issue['body'])
    if stamp_present == True:
        injected_json = extract_stamp_data(raw_issue['body'])
        raw_issue.update(injected_json)
        raw_issue['body'] = remove_stamp(raw_issue['body'])

    if user.__class__.__name__ == "AnonymousUser":
        profile = Profile.objects.get(name='Guest')
    else:
        profile = Profile.objects.get(user=user)

    profile_pk = str(profile.pk)
    injected_json = {"author":profile_pk}
    raw_issue.update(injected_json)
    serialize_github_object(repo_pk, 'serialize_repo_issue', raw_issue)


def create_issue(token, user, data, stamp, issue_id):
    g = Github(token)
    user_repo = user + '/' + data['repository'].name
    if stamp:
        body = stamp + data['body']
    else:
        body = data['body']

    repo = g.get_repo(user_repo)
    i = repo.create_issue(
        title=data['title'],
        body=body,
    )
    Issue.objects.filter(id=issue_id).update(number=i.number)


def update_issue(token, user, data, stamp, issue_number):
    g = Github(token)
    user_repo = user + '/' + data['repository'].name

    if stamp:
        body = stamp + data['body']
    else:
        body = data['body']

    repo = g.get_repo(user_repo)
    i = repo.get_issue(issue_number)
    e = i.edit(
        title=data['title'],
        body=body,
    )


def open_close_issue(token, user, state, repo, issue_number):
    g = Github(token)
    user_repo = user + '/' + repo
    repo = g.get_repo(user_repo)
    i = repo.get_issue(issue_number)
    e = i.edit(
        state=state
    )


def serialize_github_object(repo_pk, slookup, raw, path=None, file_listing=None, folder_listing=None, folder_sha=None):
    if folder_sha:
        parent_folder_pk = str(RepoFolder.objects.get(sha=folder_sha).pk)
        injected_json = {"repository":repo_pk, "parent_folder":parent_folder_pk}
    else:
        injected_json = {
            "repository":repo_pk
            }
    raw.update(injected_json)

    serializer, model = get_serializer_and_model(slookup, raw)
    if serializer.is_valid(raise_exception=True):
        if file_listing:
            saved = serializer.save(data_type=file_listing['type'])
        elif folder_listing:
            name=folder_listing['path']
            data_type=folder_listing['type']
            mode=folder_listing['mode']
            saved = serializer.save(name=name, path=path, data_type=data_type, mode=mode)
        else:
            saved = serializer.save()
