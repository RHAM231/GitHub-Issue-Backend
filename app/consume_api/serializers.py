# Django REST Imports: Logic from the Django REST Framework
from rest_framework import serializers

# Django Imports: Logic specific to this project
from issues.models import Issue, TestIssue
from users.models import Profile
from repositories.models import Repository, RepoFolder, RepoFile, LineOfCode


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''
Let's use Django REST to easily consume API data from GitHub. We define
a set of model serializers for each of our models that we're importing
GitHub data into (repositories, folders, files, lines of code). We'll
call these serializers from our github_client script in the sync app.

We'll use each serializer to create entries in our database from the
GitHub json objects.
'''

#################################################################################################################################
# BEGIN SERIALIZERS FOR CONSUMING GITHUB API DATA
#################################################################################################################################


# Define a Django REST model serializer for our issue model. This is equivalent/similiar to a Django modelform
# except for consuming json API data instead of user input data.
class IssueSerializer(serializers.ModelSerializer):
    # Declare our required foreign key fields
    repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    class Meta:
        # Set our model to recieve the data
        model = Issue
        author = serializers.CharField(read_only=True)
        
        # Declare our serializer fields the same way we would for a Django modelform
        fields = [
            'id', 'title', 'state', 'body', 'created_at', 'updated_at', 'closed_at', 
            'number', 'author', 'repository', 'associated_folder', 'associated_file', 
            'associated_loc'
            ]

    # Define custom methods for our association foreign key fields to make these fields optional
    # Folders
    def get_folder(self, obj):
        if obj.associated_folder is not None:
            return IssueSerializer(obj.associated_folder).data
        else:
            return None
    
    # Files
    def get_file(self, obj):
        if obj.associated_file is not None:
            return IssueSerializer(obj.associated_file).data
        else:
            return None
    
    # Lines of Code
    def get_loc(self, obj):
        if obj.associated_loc is not None:
            return IssueSerializer(obj.associated_loc).data
        else:
            return None


# Serializer to consume GitHub repository json objects
class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name', 'description', 'open_issues_count', 'created_at', 'updated_at', 'url']


# Serializer to consume GitHub folder json objects
class RepoFolderSerializer(serializers.ModelSerializer):
    repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    class Meta:
        model = RepoFolder
        fields = ['id', 'sha', 'url', 'repository', 'parent_folder']
    
    # Set the parent folder as an optional foreign key field
    def get_parent(self, obj):
        if obj.parent_folder is not None:
            return RepoFolderSerializer(obj.parent_folder).data
        else:
            return None


# Serializer to consume GitHub file json objects
class RepoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoFile
        fields = [
            'id', 'name', 'path', 'sha', 'url', 'data_type', 'content', 
            'encoding', 'size', 'repository', 'parent_folder'
            ]


# Define a test serializer
class TestIssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestIssue
        fields = ['id', 'title', 'state', 'body', 'number', 'created_at', 'repository_url']


#################################################################################################################################
# BEGIN SERIALIZERS FOR DISPLAYING JSON OBJECTS IN ISSUE TRACKER'S API
#################################################################################################################################


# Serializer to display issue json objects in Issue Trackers's API
class HyperlinkedIssueSerializer(serializers.HyperlinkedModelSerializer):
    # Declare our required foreign key fields
    # Set repo as hyperlinked field
    repository = serializers.HyperlinkedRelatedField(
        view_name='api-repo-detail',
        lookup_field='pk',
        queryset=Repository.objects.all()
        )
    # Set author as a display only field
    author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    # Define a link to our issue detail view
    IssueDetail = serializers.HyperlinkedIdentityField(
        view_name='api-issue-detail',
        lookup_field='pk'
    )
    # Set folder as a hyperlinked field
    associated_folder = serializers.HyperlinkedRelatedField(
        view_name='api-folder-detail',
        lookup_field='pk',
        queryset=RepoFolder.objects.all()
    )
    # Set file as a hyperlinked field
    associated_file = serializers.HyperlinkedRelatedField(
        view_name='api-file-detail',
        lookup_field='pk',
        queryset=RepoFile.objects.all()
    )
    # Set associated lines of code as a method field
    associated_loc = serializers.SerializerMethodField(
        'get_loc_line_number'
        )
    class Meta:
        # Set our model to recieve the data
        model = Issue
        
        # Declare our serializer fields the same way we would for a Django modelform
        fields = [
            'IssueDetail', 'id', 'title', 'state', 'body', 'created_at', 'updated_at', 
            'closed_at', 'number', 'author', 'repository', 'associated_folder', 
            'associated_file', 'associated_loc'
            ]
    
    # Define a method for our lines of code field to display the line of code by its
    # line number rather than its id
    def get_loc_line_number(self, obj):
        # Check if we have an associated line of code before trying to access line number
        if obj.associated_loc:
            return obj.associated_loc.line_number
        # If there's no line of code, return null
        else:
            return


# Serializer to display repository json objects in Issue Trackers's API
class HyperlinkedRepoSerializer(serializers.HyperlinkedModelSerializer):
    # Define a field to navigate to the detail view for the repo
    RepoDetail = serializers.HyperlinkedIdentityField(
        view_name='api-repo-detail',
        lookup_field='pk'
    )
    class Meta:
        model = Repository
        # Declare our display fields
        fields = ['RepoDetail', 'id', 'name', 'description', 'open_issues_count', 'created_at', 'updated_at', 'url']


# Serializer to display folder json objects in Issue Trackers's API
class HyperlinkedRepoFolderSerializer(serializers.HyperlinkedModelSerializer):
    # Define a link to our folder detail view
    FolderDetail = serializers.HyperlinkedIdentityField(
        view_name='api-folder-detail',
        lookup_field='pk'
    )
    # Display our repo field as link to that repo's detail view
    repository = serializers.HyperlinkedRelatedField(
        view_name='api-repo-detail',
        lookup_field='pk',
        queryset=Repository.objects.all()
        )
    # Same as above for the parent folder
    parent_folder = serializers.HyperlinkedRelatedField(
        view_name='api-folder-detail',
        lookup_field='pk',
        queryset=RepoFolder.objects.all()
    )
    class Meta:
        model = RepoFolder
        # Declare our display fields
        fields = ['FolderDetail', 'id', 'sha', 'url', 'repository', 'parent_folder']


# Serializer to display file json objects in Issue Trackers's API
class HyperlinkedRepoFileSerializer(serializers.HyperlinkedModelSerializer):
    # Define a link to the file's detail view
    FileDetail = serializers.HyperlinkedIdentityField(
        view_name='api-file-detail',
        lookup_field='pk'
    )
    # Display the repo field as a link to that repo's detail view
    repository = serializers.HyperlinkedRelatedField(
        view_name='api-repo-detail',
        lookup_field='pk',
        queryset=Repository.objects.all()
        )
    # Same as the repo field above
    parent_folder = serializers.HyperlinkedRelatedField(
        view_name='api-folder-detail',
        lookup_field='pk',
        queryset=RepoFolder.objects.all()
    )
    class Meta:
        model = RepoFile
        # Declare our display fields
        fields = [
            'FileDetail', 'id', 'name', 'path', 'sha', 'url', 'data_type', 'content', 
            'encoding', 'size', 'repository', 'parent_folder'
            ]


#################################################################################################################################
# END
#################################################################################################################################
