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
from consume_api.serializers import (
    IssueSerializer, TestIssueSerializer, RepoSerializer,
    RepoFolderSerializer, RepoFileSerializer,
    )


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''

'''

#################################################################################################################################
# BEGIN VIEWS
#################################################################################################################################


@api_view(['GET'])
def api_root(request, format=None):
    """
    Welcome to Issue Tracker's API written in Django REST! Here you can view Issues, 
    Repositories, Folders, and Files from the database as JSON objects.
    
    You can also perform GET, POST, and PUT operations on Issues.
    """
    # Reverse and Response are specific to DRF
    return Response({
        'issues': reverse('api-issue-list', request=request, format=format),
        'repos': reverse('api-repo-list', request=request, format=format),
        'folders': reverse('api-folder-list', request=request, format=format),
        'files': reverse('api-file-list', request=request, format=format)
    })


class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


# # Define an issue list view in our REST api to display all the issues
# class IssueList(APIView):
#     """
#     List all issues, or create a new issue. As a guest user, you can create new issues.
#     """
#     pagination_class = 'DEFAULT_PAGINATION_CLASS'
#     permission_classes = (partial(MyPermission, ['GET', 'HEAD', 'POST']),)
#     def get(self, request, format=None):
#         issues = Issue.objects.all()
#         serializer = IssueSerializer(issues, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = IssueSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define a REST api view for a single issue
class IssueDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    '''
    Display an individual issue. As a guest user, you can read and edit the issue.
    '''
    permission_classes = (partial(MyPermission, ['GET', 'HEAD', 'PUT']),)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Define views for the remaining objects, both list and detail views
class RepoList(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoFolderList(generics.ListCreateAPIView):
    queryset = RepoFolder.objects.all()
    serializer_class = RepoFolderSerializer


class RepoFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepoFolder.objects.all()
    serializer_class = RepoFolderSerializer


class RepoFileList(generics.ListCreateAPIView):
    queryset = RepoFile.objects.all()
    serializer_class = RepoFileSerializer


class RepoFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepoFile.objects.all()
    serializer_class = RepoFileSerializer


# 
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


# 
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
