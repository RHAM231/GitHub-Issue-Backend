from rest_framework import serializers
from issues.models import Issue, TestIssue
from repositories.models import Repository, RepoFolder, RepoFile


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'name', 'state', 'body', 'created_at', 'updated_at', 'closed_at', 'number', 'repository']


class TestIssueSerializer(serializers.HyperlinkedModelSerializer):
    # repository = serializers.PrimaryKeyRelatedField(queryset=Repository.objects.all())
    # highlight = serializers.HyperlinkedIdentityField(view_name='issue-highlight', format='html')
    class Meta:
        model = TestIssue
        fields = ['id', 'title', 'state', 'body', 'number', 'created_at', 'repository_url']


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name', 'description', 'open_issues_count', 'updated_at', 'url']


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
        fields = ['id', 'name', 'path', 'sha', 'url', 'data_type', 'content', 'encoding', 'size', 'repository', 'parent_folder']


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
