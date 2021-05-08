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
Let's use Django REST to easily consume API data from GitHub. We define a set of model serializers for each of our models that
we're importing GitHub data into (repositories, folders, files, lines of code). We'll call these serializers from our 
github_client script in the sync app.

We'll use each serializer to create entries in our database from the GitHub json objects.
'''

#################################################################################################################################
# BEGIN SERIALIZERS
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
    def get_folder(self, obj):
        if obj.associated_folder is not None:
            return IssueSerializer(obj.associated_folder).data
        else:
            return None
    
    def get_file(self, obj):
        if obj.associated_file is not None:
            return IssueSerializer(obj.associated_file).data
        else:
            return None
    
    def get_loc(self, obj):
        if obj.associated_loc is not None:
            return IssueSerializer(obj.associated_loc).data
        else:
            return None


# Define a test serializer
class TestIssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestIssue
        fields = ['id', 'title', 'state', 'body', 'number', 'created_at', 'repository_url']


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


#################################################################################################################################
# END
#################################################################################################################################
