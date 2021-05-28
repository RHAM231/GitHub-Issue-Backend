from issues import models as issues_models
from django.db import models
from django.utils import timezone


def type_choices():
    TYPE_CHOICES = (
        ('file', 'file'),
        ('blob', 'blob'),
        ('tree', 'tree'),
    )
    return TYPE_CHOICES


class Repository(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    open_issues_count = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=False)
    url = models.URLField(max_length=200)
    slug = models.SlugField(max_length = 200)

    def __init__(self, *args, **kwargs):
        super (Repository, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = issues_models.generate_slug(self, Repository)
        elif self.name != self.__original_name:
            self.slug = issues_models.generate_slug(self, Repository)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RepoFolder(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=150, null=True, blank=True)
    sha = models.CharField(max_length=40)
    url = models.URLField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    data_type = models.CharField(max_length=4, choices=type_choices(), default='blob')
    mode = models.CharField(max_length=100)
    issuetracker_url_path = models.CharField(max_length=150)
    slug = models.SlugField(max_length = 200)

    repository = models.ForeignKey(
        Repository,
        max_length=100,
        on_delete=models.CASCADE,
        related_name='folder_repo'
        )
    parent_folder = models.ForeignKey(
        'self',
        max_length=100,
        on_delete=models.CASCADE,
        related_name='folder_self',
        blank=True,
        null=True
        )
    
    def __init__(self, *args, **kwargs):
        super (RepoFolder, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, *args, **kwargs):
        if self.path:
            self.issuetracker_url_path = self.repository.name + '/' + self.path
        else:
            self.issuetracker_url_path = self.repository.name
        if not self.pk:
            self.slug = issues_models.generate_slug(self, RepoFolder)
        elif self.name != self.__original_name:
            self.slug = issues_models.generate_slug(self, RepoFolder)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RepoFile(models.Model):
    ENCODING_CHOICES = (
        ('base64', 'base64'),
    )
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=150)
    data_type = models.CharField(max_length=4, choices=type_choices(), default='blob')
    content = models.TextField()
    encoding = models.CharField(max_length=50, choices=ENCODING_CHOICES, default='base64')
    size = models.CharField(max_length=10)
    sha = models.CharField(max_length=40)
    url = models.URLField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    issuetracker_url_path = models.CharField(max_length=150)
    slug = models.SlugField(max_length = 200)

    repository = models.ForeignKey(
        Repository,
        max_length=100,
        on_delete=models.CASCADE,
        related_name='file_repo'
        )
    parent_folder = models.ForeignKey(
        RepoFolder,
        max_length=100,
        on_delete=models.CASCADE,
        related_name='folder_repo',
        blank=True
        )

    def __init__(self, *args, **kwargs):
        super (RepoFile, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, *args, **kwargs):
        if self.path:
            self.issuetracker_url_path = (self.repository.name + '/' + self.path).rsplit('/', 1)[0]
        else:
            self.issuetracker_url_path = self.repository.name
        if not self.pk:
            self.slug = issues_models.generate_slug(self, RepoFile)
        elif self.name != self.__original_name:
            self.slug = issues_models.generate_slug(self, RepoFile)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class LineOfCode(models.Model):
    content = models.TextField()
    line_number = models.IntegerField()
    repofile = models.ForeignKey(RepoFile, max_length=100, on_delete=models.CASCADE, related_name='loc')
    path = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.path = RepoFile.objects.get(id=self.repofile.id).issuetracker_url_path
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.line_number)
