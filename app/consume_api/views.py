from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from consume_api.serializers import (
    IssueSerializer, TestIssueSerializer, RepoSerializer,
    RepoFolderSerializer, RepoFileSerializer,
    )

from repositories.models import Repository, RepoFolder, RepoFile
from issues.models import Issue, TestIssue


# @api_view(['GET'])
# def api_root(request, format=None):
#     # Reverse and Response are specific to DRF
#     return Response({
#         'issues': reverse('issue-list', request=request, format=format),
#         # 'snippets': reverse('snippet-list', request=request, format=format)
#     })


class IssueList(APIView):
    """
    List all issues, or create a new issue.
    """
    def get(self, request, format=None):
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RepoList(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoFolderList(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoFileList(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


class RepoFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepoSerializer


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
