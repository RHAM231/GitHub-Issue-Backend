from rest_framework import serializers
from issues.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'name', 'state', 'body', 'created_at', 'updated_at', 'closed_at', 'number', 'repository']
