from django.shortcuts import render
import requests
from django.conf import settings
import os
from github import Github, GithubException
from pprint import pprint


def get_query_url(key, *args, **kwargs):
    query_dict = {
        # Rate Limit
        rate_limit: "https://api.github.com/rate_limit",

        # Repositories
        get_repo: f"https://api.github.com/repos/{owner}/{repo}",
        list_branches: f"https://api.github.com/repos/{owner}/{repo}/branches",
        get_branch: f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}",

        # Folders
        get_root_repo_tree: f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}",
        get_folder_tree: f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}",

        # Files
        get_file_contents: f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",

        # Issues
        repo_issues: f"https://api.github.com/repos/{owner}/{repo}/issues",
        create_issue: f"https://api.github.com/repos/{owner}/{repo}/issues",
        get_issue: f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_id}",
        update_issue: f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_id}",
        close_issue: f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_id}",
        open_issue: f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_id}",
    }
    url_value = query_dict.get(key, default=None)
    return url_value


def confirm_sync(request):
    api_call_result = {}
    # if request.method == 'POST':
    #     client = Github(settings.TEST_TOKEN)

    #     try:
    #         user = client.get_user(settings.USER)
    #         # api_call_result['name'] = user.name
    #         # api_call_result['login'] = user.login
    #         # api_call_result['public_repos'] = user.public_repos

    #         repo = client.get_repo('RHAM231-IssueTracker/IssueTrackerSandbox')
    #         issues = repo.get_issues(state='open')
    #         pprint(issues.get_page(0))

    #         api_call_result['success'] = True
    #         # print(api_call_result)
    #     except GithubException as ge:
    #         message = ge.data['message']
    #         print(message)
    #         api_call_result['success'] = False

    if request.method == 'POST':
        token = settings.TEST_TOKEN
        owner = settings.USER
        repo = 'IssueTrackerSandbox'
        # query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        key = 'rate_limit'
        query_url = get_query_url(key)
        params = {
            'state':'open',
        }
        headers = {'Authorization': f'token {token}'}
        # r = requests.get(query_url, headers=headers, params=params)
        r = requests.get(query_url, headers=headers)
        pprint(r.json())

    return render(request, 'sync/confirm_sync.html')


def sync_success(request):
    return render(request, 'sync/sync_success.html')



































# def github(request):
#     user = {}
#     if 'username' in request.GET:
#         username = request.GET['username']
#         url = 'https://api.github.com/users/%s' % username
#         response = requests.get(url)
#         user = response.json()
#     return render(request, 'sync/github.html', {'user': user})


def github(request):
    search_result = {}

    print('PRINTING TEST')
    test = settings.TEST
    print(test)
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
        search_result = response.json()
        search_result['success'] = search_was_successful
        search_result['rate'] = {
            'limit': response.headers['X-RateLimit-Limit'],
            'remaining': response.headers['X-RateLimit-Remaining'],
        }
    return render(request, 'sync/github.html', {'search_result': search_result})


def github_client(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        client = Github(settings.TEST_TOKEN)
        # client = Github()
        

        # repository = client.get_repo(username)
        # print(repository)

        try:
            user = client.get_user(username)
            # client.
            search_result['name'] = user.name
            search_result['login'] = user.login
            print('PRINTING LOGIN')
            print(search_result['login'])
            search_result['public_repos'] = user.public_repos
            search_result['success'] = True
        except GithubException as ge:
            search_result['message'] = ge.data['message']
            search_result['success'] = False

        # rate_limit = client.get_rate_limit()
        search_result['rate'] = {
            # 'limit': rate_limit.rate.limit,
            # 'remaining': rate_limit.rate.remaining,
        }

    return render(request, 'sync/github.html', {'search_result': search_result})