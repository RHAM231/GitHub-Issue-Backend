# Django REST Imports: Logic from the Django REST Framework
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from functools import partial

# Django Imports: Logic specific to this project
from issues.models import Issue, TestIssue
from . permissions import MyPermission
from repositories.models import Repository, RepoFolder, RepoFile
from sync.github_client import update_issue
from consume_api.serializers import (
    IssueSerializer, TestIssueSerializer, RepoSerializer,
    RepoFolderSerializer, RepoFileSerializer
    )


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''
Let's define views for displaying our database through an REST API. We use Django REST's class and function views to define an
API root view, object list views for our repos, folders, files, and issues, as well as object detail views.

These views enable GET, PUT, POST, and DELETE actions on all our database objects.
'''

#################################################################################################################################
# BEGIN VIEWS
#################################################################################################################################


# Define the api Home view
@api_view(['GET'])
def api_root(request, format=None):
    """
    Welcome to Issue Tracker's API written in Django REST. Here you can view Issues, 
    Repositories, Folders, and Files from the database as JSON objects.
    """
    # Reverse and Response are specific to DRF
    return Response({
        'issues': reverse('api-issue-list', request=request, format=format),
        'repos': reverse('api-repo-list', request=request, format=format),
        'folders': reverse('api-folder-list', request=request, format=format),
        'files': reverse('api-file-list', request=request, format=format)
    })


# Define an issue list view in our REST api to display all the issues
class IssueList(generics.ListCreateAPIView):
    """
    List all issues, or create a new issue. As a guest user, you can view issues.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


# Define an issue list view in our REST api to display all the issues
# class IssueList(APIView):
#     """
#     List all issues, or create a new issue. As a guest user, you can create new issues.
#     """
#     # pagination_class = 'DEFAULT_PAGINATION_CLASS'
#     permission_classes = (partial(MyPermission, ['GET', 'HEAD', 'POST']),)
#     def get(self, request, format=None):
#         issues = Issue.objects.all()
#         serializer = IssueSerializer(issues, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = IssueSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = Response(serializer.data, status=status.HTTP_201_CREATED)
#             print()
#             print('PRINTING SERIALIZER DATA')
#             print(serializer.data)
#             return response
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define a REST api view for a single issue
class IssueDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    '''
    Display an individual issue. As a guest user, you can view the issue.
    '''
    # permission_classes = (partial(MyPermission, ['GET', 'HEAD', 'PUT']),)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return response

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Display all the repositories in the API
class RepoList(generics.ListCreateAPIView):
    """
    List all repositories. As a guest user, you can view repositories.
    """
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


# Display an individual repository in the API
class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Display an individual repository. As a guest user, you can view the repository.
    """
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


# Display all the folders in the API
class RepoFolderList(generics.ListCreateAPIView):
    """
    List all repository folders, or create a new folder. As a guest user, you can view folders.
    """
    queryset = RepoFolder.objects.all()
    serializer_class = RepoFolderSerializer


# Display an individual folder in the API
class RepoFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Display an individual repository folder. As a guest user, you can view the folder.
    """
    queryset = RepoFolder.objects.all()
    serializer_class = RepoFolderSerializer


# Display all the files in the API
class RepoFileList(generics.ListCreateAPIView):
    """
    List all repository files, or create a new file. As a guest user, you can view files.
    """
    queryset = RepoFile.objects.all()
    serializer_class = RepoFileSerializer


# Display an individual file in the API
class RepoFileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Display an individual repository file. As a guest user, you can view the file.
    """
    queryset = RepoFile.objects.all()
    serializer_class = RepoFileSerializer


# Test Issue List View for development
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


# Test Issue Detail view for development
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


#################################################################################################################################
# END
#################################################################################################################################
