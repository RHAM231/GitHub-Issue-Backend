import datetime
import itertools
from django.urls import reverse
from django.utils import timezone,  dateformat
from django.template.defaultfilters import slugify
from django.db import models
from users.models import CustomUser
from repositories.models import RepoFile, RepoFolder, Repository, LineOfCode

# from pygments.lexers import get_all_lexers
# from pygments.styles import get_all_styles

# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class TestIssue(models.Model):
    STATE_CHOICES = (
        ('open', 'open'),
        ('closed', 'closed'),
    )
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=6, choices = STATE_CHOICES, default='open')
    body = models.TextField()
    number = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    repository_url = models.URLField(max_length=200)
    repository = models.ForeignKey(
        Repository,
        max_length=100,
        on_delete=models.CASCADE,
        related_name='testissue_repo'
        )

    # Override the model's save method so we can save and update slugs automatically
    def save(self, *args, **kwargs):
        self.repository = Repository.objects.get(url=self.repository_url)
        super().save(*args, **kwargs)

class Issue(models.Model):
    # Choices
    STATE_CHOICES = (
        ('open', 'open'),
        ('closed', 'closed'),
    )

    # Fields
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=6, choices = STATE_CHOICES, default='open')
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True) 
    number = models.IntegerField()
    slug = models.SlugField(max_length = 200)

    # Foreignkeys
    repository = models.ForeignKey(
        Repository,
        max_length=100,
        on_delete=models.CASCADE,
        related_name='issue_repo'
        )
    associated_folder = models.ForeignKey(
        RepoFolder, 
        max_length=100, 
        on_delete=models.CASCADE, 
        related_name='repofolder', 
        blank=True,
        null=True
        )
    associated_file = models.ForeignKey(
        RepoFile, 
        max_length=100, 
        on_delete=models.CASCADE, 
        related_name='repofile', 
        blank=True,
        null=True
        )
    associated_loc = models.ForeignKey(
        LineOfCode, 
        max_length=100, 
        on_delete=models.CASCADE, 
        related_name='issue_loc', 
        blank=True,
        null=True
        )
    
    # METHODS
    # Let's create unique slugs for each issue from the issue name and using itertools
    # We'll also define a method for updating slugs if the name changes
    def _generate_slug(self):
        # For larger sites we would want to define a max_length for slugs
        value = self.title
        slug_candidate = slug_original = slugify(value).upper() + '_' + str(1)
        # Count until we find an empty 'slot' for our slug
        for i in itertools.count(1):
            if not Issue.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}_{}'.format(slugify(value).title(), str(i))
        # If we're creating the first issue, set slug to default value above
        if i == 1:
            slug_new = slug_original
        # Otherwise, set it based on itertools.count()
        else:
            slug_new = slug_candidate
        self.slug = slug_new
    
    # Override the model's initialization method so we can save the orignal name.
    # Then we can compare the old with the new in the model's save method below.
    def __init__(self, *args, **kwargs):
        super (Issue, self).__init__(*args, **kwargs)
        self.__original_title = self.title
        self.__original_associated_folder = self.associated_folder
        self.__original_associated_file = self.associated_file
        self.__original_associated_loc = self.associated_loc

    # Override the model's save method so we can save and update slugs automatically
    def save(self, *args, **kwargs):
        # If we're creating the issue for the first time, generate a slug
        if not self.pk:
            self._generate_slug()
        # Else if we changed the name, generate a slug
        elif self.title != self.__original_title:
            self._generate_slug()

        print(self.__original_associated_folder)

        old_associations = [self.__original_associated_folder, self.__original_associated_file, self.__original_associated_loc]
        new_associations = [self.associated_folder, self.associated_file, self.associated_loc]

        if any([
            self.__original_associated_folder != self.associated_folder, 
            self.__original_associated_file != self.associated_file, 
            self.__original_associated_loc != self.associated_loc
            ]):

        # if anything changes, determine whether the change was to add, update, or delete a stamp
        # if adding, create as normal (if orignal were all none and if any of the new 3 are not none)
        # if updating, delete the old stamp and create as normal (if any orignal were not none, and any new are not none)
        # if deleting, delete the old stamp (if all 3 new are none)
            if any([old_associations] == None):
                print('all old_associations are none')

                # if self.body:
                #     stamp_id = str(1234567812345678)
                #     stamp = 'Stamp Id: ' + stamp_id
                #     if stamp in self.body:
                #         print('Stamp exists, do nothing')
                #         self.body = self.body
                #     else:
                #         print('Stamp not present, trying to adding it ... ')

                #         if self.associated_folder:
                #             if self.associated_folder.path:
                #                 full_path = str(self.repository.name) + '/' + str(self.associated_folder.path)
                #             else:
                #                 full_path = str(self.repository.name)
                #             folder_name = str(self.associated_folder.name)
                #             file_name = 'None'
                #             loc = 'None'

                #             if self.associated_file:
                #                 self.associated_folder = self.associated_file.parent_folder
                #                 full_path = str(self.associated_file.repository.name) + '/' + str(self.associated_file.path)
                #                 file_name = str(self.associated_file.name)

                #                 if self.associated_loc:
                #                     self.associated_file = self.associated_loc.repofile
                #                     self.associated_folder = self.associated_file.parent_folder
                #                     loc = str(self.associated_loc.line_number)

                #         date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')

                #         stamp = (
                #             'Issue Location: ' + full_path + '\n' +
                #             'Affected Folder: ' + folder_name + '\n' +
                #             'Affected File: ' + file_name + '\n' +
                #             'Affected Line of Code: ' + loc + '\n' +
                #             'Generated by Issue Tracker: ' + date + '\n' +
                #             'Stamp Id: ' + stamp_id + '\n' +
                #             '\n'
                #         )

                #         self.body = stamp + self.body








        super().save(*args, **kwargs)
    
    # Built in redirect for create view
    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'issue_slug': self.slug})

    # Define which attribute the issue will be listed by in the admin portion of the site
    def __str__(self):
        return self.title
