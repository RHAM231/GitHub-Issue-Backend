from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    open_issues_count = models.CharField(max_length=100)
    # updated_at = 

    def __str__(self):
        return self.name


class RepoFolder(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    sha = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RepoFile(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    encoding = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    sha = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name
