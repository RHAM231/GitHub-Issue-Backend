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

'''

#################################################################################################################################
# BEGIN SERIALIZERS
#################################################################################################################################


class IssueSerializer(serializers.ModelSerializer):
    # associated_folder = serializers.PrimaryKeyRelatedField(queryset=RepoFolder.objects.all())
    # associated_file = serializers.PrimaryKeyRelatedField(queryset=RepoFile.objects.all())
    # associated_loc = serializers.PrimaryKeyRelatedField(queryset=LineOfCode.objects.all())
    repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'state', 'body', 'created_at', 'updated_at', 'closed_at', 
            'number', 'author', 'repository', 'associated_folder', 'associated_file', 'associated_loc'
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


class TestIssueSerializer(serializers.HyperlinkedModelSerializer):
    # repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    # highlight = serializers.HyperlinkedIdentityField(view_name='issue-highlight', format='html')
    class Meta:
        model = TestIssue
        fields = ['id', 'title', 'state', 'body', 'number', 'created_at', 'repository_url']


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name', 'description', 'open_issues_count', 'created_at', 'updated_at', 'url']


class RepoFolderSerializer(serializers.ModelSerializer):
    repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    # parent_folder = serializers.PrimaryKeyRelatedField(queryset=RepoFolder.objects.all())
    class Meta:
        model = RepoFolder
        fields = ['id', 'sha', 'url', 'repository', 'parent_folder']
    
    def get_parent(self, obj):
        if obj.parent_folder is not None:
            return RepoFolderSerializer(obj.parent_folder).data
        else:
            return None

    # def save(self):
    #     repository = self.repo_obj



class RepoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoFile
        fields = [
            'id', 'name', 'path', 'sha', 'url', 'data_type', 'content', 
            'encoding', 'size', 'repository', 'parent_folder'
            ]


    # def create(self, validated_data, **kwargs):
    #     repo_obj = Repository.objects.get(id=validated_data["repository"])
    #     testissue = TestIssue.objects.create(
    #         name=validated_data["name"],
    #         state=validated_data["state"],
    #         body=validated_data["body"],
    #         number=validated_data["number"],
    #         repository=repo_obj
    #     )
    #     return testissue


# class TestIssueSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     state = serializers.CharField(max_length=100)
#     body = serializers.CharField()
#     number = serializers.IntegerField()
#     repository = serializers.CharField(source='repository.name')

#     def create(self, validated_data):
#         """
#         Create and return a new `TestIssue` instance, given the validated data.
#         """
#         return TestIssue.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `TestIssue` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.state = validated_data.get('state', instance.state)
#         instance.body = validated_data.get('body', instance.body)
#         instance.number = validated_data.get('number', instance.number)
#         instance.repository = validated_data.get('repository', instance.name) #FIXME
#         instance.save()
#         return instance


#################################################################################################################################
# END
#################################################################################################################################
