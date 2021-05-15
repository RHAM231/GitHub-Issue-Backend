# Python Imports
import os
import base64
import requests
from pprint import pprint
from github import Github, GithubException

# Django Imports: Logic specific to this project
from issues.models import Issue
from users.models import Profile
from repositories.models import Repository, RepoFolder, RepoFile, LineOfCode
from consume_api.serializers import RepoSerializer, RepoFolderSerializer, RepoFileSerializer, IssueSerializer


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''
Let's build a client for retrieving a GitHub repository and all its folders and files.

First we define two Dictionary lookup methods, get_query_url(), and get_serializer_and_model() for managing our data that we use
to retrieve and serialize GitHub objects. We'll call the first method to get GitHub API endpoints, then use these endpoinnts to
retrieve GitHub objects. Next, we'll call our second method to get the appropriate Django REST serializer and Django model to 
save the GitHub object to our database.

To retrieve GitHub objects from their API, we define a series of "get" methods for the repository, repository root folder, and 
the folders and files. We also define an unpack_repository() method which we will call recursively to iterate through all the 
folders and files.

Finally we define a serialize_github_object_method() for dumping our retrieved json objects to our database while the unpack
method is running.

We also define a method for decoding and saving all the individual lines of code for each GitHub file we serialize.

We start this entire process by calling the get_repo() method from our views.py file in this app
'''


#################################################################################################################################
# BEGIN SCRIPT
#################################################################################################################################


# Given a query url lookup string and additional needed parameters, return an endpoint for
# retrieving GitHub objects from GitHub's API.
def get_query_url(lookup, branch=None, sha=None, path=None, issue_id=None):
    # Define our base endpoint
    endpoint = "https://api.github.com/repos/RHAM231-IssueTracker/IssueTrackerSandbox"
    # Define a dictionary linking lookups to endpoints
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
    }
    # Return our endpoint based on lookup
    url_value = query_dict.get(lookup, None)
    return url_value


# Given a serializer lookup string and a raw json object, return a tuple 
# containing the appropriate Django REST serializer and Django model
def get_serializer_and_model(slookup, raw):
    # Define a dictionary linking lookup to tuple
    serializer_model_dict = {
        # Repositories
        'serialize_repo': (RepoSerializer(data=raw), Repository),
        # Folders
        'serialize_folder_tree': (RepoFolderSerializer(data=raw), RepoFolder),
        # Files
        'serialize_file_contents': (RepoFileSerializer(data=raw), RepoFile),
        # Issues
        'serialize_repo_issue': (IssueSerializer(data=raw), Issue),
    }
    # Return our serializer and model based on lookup
    serializer_and_model = serializer_model_dict.get(slookup, None)
    return serializer_and_model


# Define our get GitHub repository method.
def get_repo(lookup, headers, user):
    # Given a lookup, retrieve our query url, get our repo, and convert it to json
    query_url = get_query_url(lookup)
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    # Pull some additional parameters out of the json that we'll need later
    repo_url = raw['url']
    repo_branch = raw['default_branch']

    # For development/testing, purge our database on each new retrieval
    Repository.objects.all().delete()

    # Now call our serializer method. We'll serialize the repo independently 
    # from our serialize_github_object() method below because this is an edge case.
    serializer = RepoSerializer(data=raw)
    if serializer.is_valid():
        serializer.save()
    
    # Use our json url parameter from above to get the repo's new primary key
    # from our database
    repo_pk = str(Repository.objects.get(url=repo_url).pk)

    # Now call our root folder method. Pass our extra parameters so we can continue
    # getting and serializing github objects.
    get_root_folder(repo_pk, repo_branch, headers)
    get_repo_issues('get_repo_issues', repo_pk, headers, user)


# Define a method for retrieving the root folder of a GitHub repository
def get_root_folder(repo_pk, repo_branch, headers):
    # Get the GitHub project's main branch so we can access the root folder sha
    query_url_branch = get_query_url('get_branch', branch=repo_branch)
    main_branch = requests.get(query_url_branch, headers=headers)
    raw_branch = main_branch.json()
    root_folder_sha = raw_branch['commit']['commit']['tree']['sha']

    # Use the root folder sha to get the root folder
    query_url_root = get_query_url('get_root_repo_tree', sha=root_folder_sha)
    root_folder = requests.get(query_url_root, headers=headers)
    raw_folder = root_folder.json()
    injected_json = {"repository":repo_pk, "parent_folder":None}
    raw_folder.update(injected_json)

    # For testing/development purposes, let's flush our models before we save new objects
    RepoFolder.objects.all().delete()
    RepoFile.objects.all().delete()

    # Now save our root folder to database using a Django REST serializer
    serializer = RepoFolderSerializer(data=raw_folder)
    if serializer.is_valid():
        saved = serializer.save(name='repo_root', path='', data_type='tree', mode='040000')
    
    # Call our recursive method to begin retrieving and saving the repository folders and files
    unpack_repository(repo_pk, raw_folder, headers, '')


# Define our recursive method for unpacking a GitHub repo. Give it a folder, current path
# and headers to pass to our get_repofile and get_repofolder methods. 
def unpack_repository(repo_pk, folder, headers, current_path):
    # pull our tree and sha out of our json folder
    tree = folder['tree']
    folder_sha = folder['sha']
    for entry in tree:
        # if a tree object is a file, call our get_repofile method, passing headers and current path
        # to it so it can get the file from GitHub. Pass sha so it can serialize the file to database.
        if entry['type'] == 'blob':
            get_repofile(repo_pk, entry, headers, folder_sha, current_path)
        # if our object is a folder, call our get_repofolder method instead
        elif entry['type'] == 'tree':
            get_repofolder(repo_pk, entry, headers, folder_sha, current_path)


# Define a get folder method to get a single folder from GitHub, serialize it to database, and call our
# unpack method again if needed to get the folder's contents.
def get_repofolder(repo_pk, folder_listing, headers, folder_sha, current_path):
    # Get our current folder sha from the previous folder tree we got from calling the unpack method
    current_sha = folder_listing['sha']
    # Define our query url using the sha and our get_query_url method defined above
    query_url = get_query_url('get_folder_tree', sha=current_sha)

    # Get the folder from GitHub using our query url and headers and convert it to raw json
    r = requests.get(query_url, headers=headers)
    raw_subfolder = r.json()

    # Dump our new json object into our database by calling our serialize_github_object method,
    # giving it whatever additional parameters it needs to save the object
    print('serializing a folder ...')
    serialize_github_object(
        repo_pk, 'serialize_folder_tree', raw_subfolder, path=current_path,
        folder_listing=folder_listing, folder_sha=folder_sha
        )

    # Now that we've retrieved and saved the folder, we need to retrieve and save it's contents.
    # If we came from the root folder, add our current subfolder name to the the current path
    if current_path == '':
        current_path = current_path + folder_listing['path']
    # Otherwise, append our current subfolder to path with a slash
    else:
        current_path = current_path + '/' + folder_listing['path']
    # Now call our unpack method again, giving it our current subfolder and our new path.
    unpack_repository(repo_pk, raw_subfolder, headers, current_path)


# Define a get file method for retrieving and serializing a GitHub file
def get_repofile(repo_pk, file_listing, headers, folder_sha, current_path):
    # Add our file name to the current path so we can retrieve it from GitHub
    if current_path == '':
        path = current_path + file_listing['path']
    else:
        path = current_path + '/' + file_listing['path']
    # Construct our query url from our get url method and our current path
    query_url = get_query_url('get_file_contents', path=path)
    
    # Retrieve the file from GitHub, convert to json, and then serialize to database with our serialize object method
    r = requests.get(query_url, headers=headers)
    raw_file = r.json()

    serialize_github_object(
        repo_pk, 'serialize_file_contents', raw_file, 
        file_listing=file_listing, folder_sha=folder_sha
        )
    
    # Now that we've saved our file to database, let's save indivdual lines of code.
    # Get our file content and lookup parameters
    file_content = raw_file['content']
    file_sha = raw_file['sha']
    file_path = raw_file['path']

    # Get our parent file so we can save lines of code. Lookup by two parameters because GitHub
    # shas are not always unique.
    parent_file = RepoFile.objects.get(sha=file_sha, path=file_path)
    # Call our save lines of code method
    save_locs(file_content, parent_file)
    

# Given encoded file content and the parent file from our database, decode and save the content
# as individual lines of code
def save_locs(content, parent_file):
    # Decode our content
    decoded = base64.b64decode(content)
    # Get a list of the lines
    lines_of_code = [item.decode('utf-8') for item in decoded.splitlines()]

    # Save all the lines to database with a foreign key relation to its file
    for i, line in enumerate(lines_of_code):
        new_line = LineOfCode(content=line, line_number=i, repofile=parent_file)
        new_line.save()


# Given necessary lookup parameters, get all the GitHub issues from a repository
# and call our get_issue() method for each issue
def get_repo_issues(lookup, repo_pk, headers, user):
    query_url = get_query_url(lookup)
    r = requests.get(query_url, headers=headers)
    raw_issues_list = r.json()
    issue_numbers = [issue['number'] for issue in raw_issues_list]
    issue_numbers.reverse()
    for number in issue_numbers:
        get_issue('get_issue', repo_pk, headers, number, user)


# Run a series of checks to see if our GitHub issue contains a stamp
# generated by Issue Tracker. Return true if present and false if not
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


# If an Issue Tracker generated stamp is present in our issue, we're importing from GitHub.
# Get all the stamp data so we can inject it as json before serializing our issue to the
# database.
def extract_stamp_data(body):
    # Get our stamp data
    path = (body.splitlines()[0]).replace('Issue Location: ', '')
    folder = (body.splitlines()[1]).replace('Affected Folder: ', '')
    file = (body.splitlines()[2]).replace('Affected File: ', '')
    loc = (body.splitlines()[3]).replace('Affected Line of Code: ', '')

    # Based on the stamp data, set the injected json accordingly
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

    # Send our injected json back to our get_issue() method
    return injected_json


# Define a method to remove an Issue Tracker stamp from the imported GitHub issue body
# before saving the issue to the database
def remove_stamp(body):
    nlines = body.count('\n')
    if nlines == 5:
        body = ''
    else:
        body = body.split('\n',7)[7]
    return body


# Given individual issue parameters, retrieve the single issue from GitHub as
# a json object and serialize it to the database by calling our serialize method
def get_issue(lookup, repo_pk, headers, issue_id, user):
    query_url = get_query_url(lookup, issue_id=issue_id)
    r = requests.get(query_url, headers=headers)
    raw_issue = r.json()

    # Check if the GitHub issue as an Issue Tracker stamp
    stamp_present = check_for_stamp(raw_issue['body'])
    # If the stamp is present, extract the stamp data to inject in our json object
    # so we can serialize the correct fields
    if stamp_present == True:
        injected_json = extract_stamp_data(raw_issue['body'])
        raw_issue.update(injected_json)
        # Finally, remove the stamp from the body before serializing
        raw_issue['body'] = remove_stamp(raw_issue['body'])


    # Check wether the user is a guest or is logged in and get the profile
    if user.__class__.__name__ == "AnonymousUser":
        profile = Profile.objects.get(name='Guest')
    else:
        profile = Profile.objects.get(user=user)

    # Use our profile to get the profile primary key and inject this into our json issue.
    # We do this to work around Django REST being difficult to use when serializing extra
    # foriegn keys.
    profile_pk = str(profile.pk)
    injected_json = {"author":profile_pk}
    raw_issue.update(injected_json)

    # Now serialize the issue using Django REST
    print('serializing an issue ...')
    serialize_github_object(repo_pk, 'serialize_repo_issue', raw_issue)


# Given data from our frontend issue creation form, use the 3rd party module, 
# GitHub, to create a new issue on GitHub
def create_issue(token, user, data, stamp, issue_id):
    # Set attributes we will use to get the repo and create the issue
    g = Github(token)
    user_repo = user + '/' + data['repository'].name
    if stamp:
        body = stamp + data['body']
    else:
        body = data['body']

    # Use the Python GitHub package to create our issue on GitHub
    repo = g.get_repo(user_repo)
    i = repo.create_issue(
        title=data['title'],
        body=body,
    )
    # Grab the returned issue number from GitHub and update our 
    # own database instance with it
    Issue.objects.filter(id=issue_id).update(number=i.number)


# Given data from our frontend, edit an existing issue on GitHub
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


# Given data from our frontend, open or close an existing issue on GitHub
def open_close_issue(token, user, state, repo, issue_number):
    g = Github(token)
    user_repo = user + '/' + repo
    repo = g.get_repo(user_repo)
    i = repo.get_issue(issue_number)
    e = i.edit(
        state=state
    )


# Define a method for serializing raw json output from our get methods above
def serialize_github_object(repo_pk, slookup, raw, path=None, file_listing=None, folder_listing=None, folder_sha=None):
    # Get the primary key of our parent folder from our database by its sha. Convert to string.
    if folder_sha:
        parent_folder_pk = str(RepoFolder.objects.get(sha=folder_sha).pk)
    
    # GitHub's API stores children information in parent objects rather than parent information in children objects. 
    # As a result, we need to inject all parent information into our database objects as additional parameters when
    # we serialize. Normally we use the serializer's save method to do this. But this method doesn't appear to work
    # for foreign key relations. As a workaround, we inject the fk parameters directly into the raw json before call-
    # ing the serializer.
        injected_json = {"repository":repo_pk, "parent_folder":parent_folder_pk}
    else:
        injected_json = {
            "repository":repo_pk
            }
    raw.update(injected_json)

    # Now we can call our serializer. We use our serializer/model lookup method to match the raw json object
    # with its appropriate serializer and model.
    serializer, model = get_serializer_and_model(slookup, raw)
    # Now we check validity and type, then save with additional parameters
    if serializer.is_valid(raise_exception=True):
        if file_listing:
            # Save a file object with the extra data_type parameter obtained from its parent GitHub tree
            saved = serializer.save(data_type=file_listing['type'])
        elif folder_listing:
            # Save a folder object with additional parameters obtained from its parent GitHub tree
            name=folder_listing['path']
            data_type=folder_listing['type']
            mode=folder_listing['mode']
            saved = serializer.save(name=name, path=path, data_type=data_type, mode=mode)
        else:
            saved = serializer.save()


#################################################################################################################################
# END
#################################################################################################################################
