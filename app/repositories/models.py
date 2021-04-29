# from issues.methods import generate_slug
from django.db import models



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
    updated_at = models.DateTimeField(auto_now=False)
    url = models.URLField(max_length=200)
    slug = models.SlugField(max_length = 200, unique=True)

    # Methods
    # Override the model's initialization method so we can check for changes in values
    # we want to save with custom methods
    def __init__(self, *args, **kwargs):
        super (Repository, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    # Override the model's save method so we can include custom save methods
    def save(self, *args, **kwargs):
        # If we're creating the object for the first time, generate a slug
        if not self.pk:
            self.slug = generate_slug(self, Repository)
        # Else if we changed the name, generate a slug
        elif self.name != self.__original_name:
            self.slug = generate_slug(self, Repository)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RepoFolder(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=150)
    sha = models.CharField(max_length=40)
    url = models.URLField(max_length=250)
    data_type = models.CharField(max_length=4, choices=type_choices(), default='blob')
    mode = models.CharField(max_length=100)

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

    def __str__(self):
        return self.name


class LineOfCode(models.Model):
    content = models.CharField(max_length=255)
    line_number = models.IntegerField()
    repofile = models.ForeignKey(RepoFile, max_length=100, on_delete=models.CASCADE, related_name='loc')

    def __str__(self):
        return str(self.line_number)
