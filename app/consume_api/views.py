from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from issues.models import Issue, TestIssue
from repositories.models import Repository, RepoFolder, RepoFile
from consume_api.serializers import (
    HyperlinkedIssueSerializer, TestIssueSerializer, HyperlinkedRepoSerializer,
    HyperlinkedRepoFolderSerializer, HyperlinkedRepoFileSerializer
    )


@api_view(['GET'])
def api_root(request, format=None):
    """
    Welcome to Issue Tracker's API built using Django REST. Here you can view Issues, 
    Repositories, Folders, and Files from the database as JSON objects.
    """

    return Response({
        'issues': reverse('api-issue-list', request=request, format=format),
        'repos': reverse('api-repo-list', request=request, format=format),
        'folders': reverse('api-folder-list', request=request, format=format),
        'files': reverse('api-file-list', request=request, format=format)
    })


class IssueList(generics.ListCreateAPIView):
    """
    List all issues, or create a new issue. As a guest user, you can view issues 
    and navigate to other JSON objects using these issues' links.
    """
    queryset = Issue.objects.all()
    serializer_class = HyperlinkedIssueSerializer


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Display an individual issue. As a guest user, you can view the issue and navigate 
    to other JSON objects using this issue's links.
    '''
    queryset = Issue.objects.all()
    serializer_class = HyperlinkedIssueSerializer


class RepoList(generics.ListCreateAPIView):
    """
    List all repositories. As a guest user, you can view repositories and navigate to other 
    JSON objects using these repos' links.
    
    The 'url' field is a GitHub API endpoint and will take you out of Issue Tracker's API.
    """
    queryset = Repository.objects.all()
    serializer_class = HyperlinkedRepoSerializer


class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Display an individual repository. As a guest user, you can view the repository
    and navigate to other JSON objects using this repo's links.
    
    The 'url' field is a GitHub API endpoint and will take you out of Issue Tracker's API.
    """
    queryset = Repository.objects.all()
    serializer_class = HyperlinkedRepoSerializer


class RepoFolderList(generics.ListCreateAPIView):
    """
    List all repository folders, or create a new folder. As a guest user, you can view folders
    and navigate to other JSON objects using these folders' links.
    
    The 'url' field is a GitHub API endpoint and will take you out of Issue Tracker's API.
    """
    queryset = RepoFolder.objects.all()
    serializer_class = HyperlinkedRepoFolderSerializer


class RepoFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Display an individual repository folder. As a guest user, you can view the folder
    and navigate to other JSON objects using this folder's links.
    
    The 'url' field is a GitHub API endpoint and will take you out of Issue Tracker's API.
    """
    queryset = RepoFolder.objects.all()
    serializer_class = HyperlinkedRepoFolderSerializer


class RepoFileList(generics.ListCreateAPIView):
    """
    List all repository files, or create a new file. As a guest user, you can view files
    and navigate to other JSON objects using these object's links.
    
    The 'url' field is a GitHub API endpoint and will take you out of Issue Tracker's API.
    """
    queryset = RepoFile.objects.all()
    serializer_class = HyperlinkedRepoFileSerializer


class RepoFileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Display an individual repository file as a JSON object. As a guest user, you can view 
    the file and navigate to other JSON objects using this object's links.
    
    The 'url' field is a GitHub API endpoint and will take you out of Issue Tracker's API.
    """
    queryset = RepoFile.objects.all()
    serializer_class = HyperlinkedRepoFileSerializer


class TestIssueList(APIView):
    """
    List all test issues, or create a new test issue.
    """
    def get(self, request, format=None):
        test_issues = TestIssue.objects.all()
        serializer = TestIssueSerializer(test_issues, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TestIssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestIssueDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = TestIssue.objects.all()
    serializer_class = TestIssueSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
