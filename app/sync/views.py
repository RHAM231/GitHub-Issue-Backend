# Django Imports: Logic from the Django Framework
from django.conf import settings
from django.shortcuts import render

# Django Imports: Logic specific to this project
from . github_client import (
    get_query_url, get_serializer_and_model, get_root_folder, 
    get_repo, get_repo_issues, create_issue, update_issue
    )


# 
def confirm_sync(request):
    if request.method == 'POST':
        token = settings.TEST_TOKEN
        headers = {
            'Authorization': f'token {token}',
            }
        # update_issue(token, 6)
        # get_repo('get_repo', headers)
        # get_root_folder(headers)
        return render(request, 'sync/sync_success.html')

    return render(request, 'sync/confirm_sync.html')


# 
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