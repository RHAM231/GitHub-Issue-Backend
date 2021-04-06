# Python Imports
import os
import requests
from pprint import pprint

# Django Imports: Logic specific to this project
from issues.models import Issue
from repositories.models import Repository, RepoFolder, RepoFile
from consume_api.serializers import RepoSerializer, RepoFolderSerializer, RepoFileSerializer, IssueSerializer


#################################################################################################################################
# INTRODUCTION
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
        'close_issue': endpoint + f'/issues/{issue_id}',
        'open_issue': endpoint + f'/issues/{issue_id}',
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
    # Return our serializer and model based on lookup
    serializer_and_model = serializer_model_dict.get(slookup, None)
    return serializer_and_model


# Define our get GitHub repository method.
def get_repo(lookup):
    # Given a lookup, retrieve our query url, get our repo, and convert it to json
    query_url = get_query_url(lookup)
    r = requests.get(query_url, headers=headers)
    raw = r.json()
    # Now call our serializer method
    serializer = RepoSerializer(data=raw)
    if serializer.is_valid():
        Repository.objects.all().delete()
        saved = serializer.save()


# Define a method for retrieving the root folder of a GitHub repository
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
    injected_json = {"repository":"1", "parent_folder":None}
    raw_folder.update(injected_json)

    # For testing/development purposes, let's flush our models before we save new objects
    RepoFolder.objects.all().delete()
    RepoFile.objects.all().delete()

    # Now save our root folder to database using a Django REST serializer
    serializer = RepoFolderSerializer(data=raw_folder)
    if serializer.is_valid():
        saved = serializer.save(name='repo_root', path='tbd', data_type='tree', mode='040000')
    
    # Call our recursive method to begin retrieving and saving the repository folders and files
    unpack_repository(raw_folder, headers, '')


# Define our recursive method for unpacking a GitHub repo. Give it a folder, current path
# and headers to pass to our get_repofile and get_repofolder methods. 
def unpack_repository(folder, headers, current_path):
    # pull our tree and sha out of our json folder
    tree = folder['tree']
    folder_sha = folder['sha']
    for entry in tree:
        # if a tree object is a file, call our get_repofile method, passing headers and current path
        # to it so it can get the file from GitHub. Pass sha so it can serialize the file to database.
        if entry['type'] == 'blob':
            get_repofile(entry, headers, folder_sha, current_path)
        # if our object is a folder, call our get_repofolder method instead
        elif entry['type'] == 'tree':
            get_repofolder(entry, headers, folder_sha, current_path)


# Define a get folder method to get a single folder from GitHub, serialize it to database, and call our
# unpack method again if needed to get the folder's contents.
def get_repofolder(folder_listing, headers, folder_sha, current_path):
    # Get our current folder sha from the previous folder tree we got from calling the unpack method
    current_sha = folder_listing['sha']
    # Define our query url using the sha and our get_query_url method defined above
    query_url = get_query_url('get_folder_tree', sha=current_sha)

    # Get the folder from GitHub using our query url and headers and convert it to raw json
    r = requests.get(query_url, headers=headers)
    raw_subfolder = r.json()

    # Dump our new json object into our database by calling our serialize_github_object method,
    # giving it whatever additional parameters it needs to save the object
    serialize_github_object(
        'serialize_folder_tree', raw_subfolder, 
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
    unpack_repository(raw_subfolder, headers, current_path)


# Define a get file method for retrieving and serializing a GitHub file
def get_repofile(file_listing, headers, folder_sha, current_path):
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
    serialize_github_object('serialize_file_contents', raw_file, file_listing=file_listing, folder_sha=folder_sha)


# Define a method for serializing raw json output from our get methods above
def serialize_github_object(slookup, raw, file_listing=None, folder_listing=None, folder_sha=None):
    # Get the primary key of our parent folder from our database by its sha. Convert to string.
    parent_folder_pk = str(RepoFolder.objects.get(sha=folder_sha).pk)
    # GitHub's API stores children information in parent objects rather than parent information in children objects. 
    # As a result, we need to inject all parent information into our database objects as additional parameters when
    # we serialize. Normally we use the serializer's save method to do this. But this method doesn't appear to work
    # for foreign key relations. As a workaround, we inject the fk parameters directly into the raw json before call-
    # ing the serializer.
    injected_json = {"repository":"1", "parent_folder":parent_folder_pk}
    raw.update(injected_json)

    # Now we can call our serializer. We use our serializer/model lookup method to match the raw json object
    # with its appropriate serializer and model.
    serializer, model = get_serializer_and_model(slookup, raw)
    
    # Now we check validity and type, then save with additional parameters
    if serializer.is_valid():
        if file_listing:
            # Save a file object with the extra data_type parameter obtained from its parent GitHub tree
            saved = serializer.save(data_type=file_listing['type'])
        elif folder_listing:
            # Save a folder object with additional parameters obtained from its parent GitHub tree
            name=folder_listing['path']
            path='tbd'
            data_type=folder_listing['type']
            mode=folder_listing['mode']
            saved = serializer.save(name=name, path=path, data_type=data_type, mode=mode)
        else:
            saved = serializer.save()

#################################################################################################################################
# END
#################################################################################################################################
