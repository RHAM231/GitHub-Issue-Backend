from rest_framework import serializers
from issues.models import Issue, TestIssue
from users.models import Profile
from repositories.models import Repository, RepoFolder, RepoFile, LineOfCode


class IssueSerializer(serializers.ModelSerializer):
    repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    class Meta:
        model = Issue
        author = serializers.CharField(read_only=True)
        fields = [
            'id', 'title', 'state', 'body', 'created_at', 'updated_at', 'closed_at', 
            'number', 'author', 'repository', 'associated_folder', 'associated_file', 
            'associated_loc'
            ]

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


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name', 'description', 'open_issues_count', 'created_at', 'updated_at', 'url']


class RepoFolderSerializer(serializers.ModelSerializer):
    repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    class Meta:
        model = RepoFolder
        fields = ['id', 'sha', 'url', 'repository', 'parent_folder']
    
    def get_parent(self, obj):
        if obj.parent_folder is not None:
            return RepoFolderSerializer(obj.parent_folder).data
        else:
            return None


class RepoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoFile
        fields = [
            'id', 'name', 'path', 'sha', 'url', 'data_type', 'content', 
            'encoding', 'size', 'repository', 'parent_folder'
            ]


class TestIssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestIssue
        fields = ['id', 'title', 'state', 'body', 'number', 'created_at', 'repository_url']


class HyperlinkedIssueSerializer(serializers.HyperlinkedModelSerializer):
    repository = serializers.HyperlinkedRelatedField(
        view_name='api-repo-detail',
        lookup_field='pk',
        queryset=Repository.objects.all()
        )
    author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    IssueDetail = serializers.HyperlinkedIdentityField(
        view_name='api-issue-detail',
        lookup_field='pk'
    )
    associated_folder = serializers.HyperlinkedRelatedField(
        view_name='api-folder-detail',
        lookup_field='pk',
        queryset=RepoFolder.objects.all()
    )
    associated_file = serializers.HyperlinkedRelatedField(
        view_name='api-file-detail',
        lookup_field='pk',
        queryset=RepoFile.objects.all()
    )
    associated_loc = serializers.SerializerMethodField(
        'get_loc_line_number'
        )
    class Meta:
        model = Issue
        fields = [
            'IssueDetail', 'id', 'title', 'state', 'body', 'created_at', 'updated_at', 
            'closed_at', 'number', 'author', 'repository', 'associated_folder', 
            'associated_file', 'associated_loc'
            ]
    
    def get_loc_line_number(self, obj):
        if obj.associated_loc:
            return obj.associated_loc.line_number
        else:
            return


class HyperlinkedRepoSerializer(serializers.HyperlinkedModelSerializer):
    RepoDetail = serializers.HyperlinkedIdentityField(
        view_name='api-repo-detail',
        lookup_field='pk'
    )
    class Meta:
        model = Repository
        fields = ['RepoDetail', 'id', 'name', 'description', 'open_issues_count', 'created_at', 'updated_at', 'url']


class HyperlinkedRepoFolderSerializer(serializers.HyperlinkedModelSerializer):
    FolderDetail = serializers.HyperlinkedIdentityField(
        view_name='api-folder-detail',
        lookup_field='pk'
    )
    repository = serializers.HyperlinkedRelatedField(
        view_name='api-repo-detail',
        lookup_field='pk',
        queryset=Repository.objects.all()
        )
    parent_folder = serializers.HyperlinkedRelatedField(
        view_name='api-folder-detail',
        lookup_field='pk',
        queryset=RepoFolder.objects.all()
    )
    class Meta:
        model = RepoFolder
        fields = ['FolderDetail', 'id', 'sha', 'url', 'repository', 'parent_folder']


class HyperlinkedRepoFileSerializer(serializers.HyperlinkedModelSerializer):
    FileDetail = serializers.HyperlinkedIdentityField(
        view_name='api-file-detail',
        lookup_field='pk'
    )
    repository = serializers.HyperlinkedRelatedField(
        view_name='api-repo-detail',
        lookup_field='pk',
        queryset=Repository.objects.all()
        )
    parent_folder = serializers.HyperlinkedRelatedField(
        view_name='api-folder-detail',
        lookup_field='pk',
        queryset=RepoFolder.objects.all()
    )
    class Meta:
        model = RepoFile
        fields = [
            'FileDetail', 'id', 'name', 'path', 'sha', 'url', 'data_type', 'content', 
            'encoding', 'size', 'repository', 'parent_folder'
            ]
