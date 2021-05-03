# Python Imports
import datetime
import itertools

# Django Imports: Logic from the Django Framework
from django.urls import reverse
from django.utils import timezone,  dateformat
from django.template.defaultfilters import slugify
from django.db import models

# Django Imports: Logic specific to this project
from users.models import CustomUser, Profile
from repositories.models import RepoFile, RepoFolder, Repository, LineOfCode


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''
Let's define our Issue model with a generate_slug method and a set of custom stamping methods. We set up fields to store the 
GitHub data we need and add the additional foreign key fields of associated files, folders, and lines of code. Because we're 
adding fields, we need a way to store this extra information in GitHub issues when we sync and send our edited or 
updated issues back to GitHub.

We will do this by "stamping" our issues with the extra data if we introduce any of the new associations. We define a set of 
custom CRUD methods for working with stamps and tie these into our Issue model by overriding its __init__ and save methods.

If adding or updating Issue associations, we will generate a stamp and append it to the top of the issue body. If deleting, we 
will remove the stamp.
'''

#################################################################################################################################
# BEGIN SCRIPT
#################################################################################################################################


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


# Given all the necessary stamp parameters, set our stamp and return it to our
# create stamp method below
def set_stamp(path, folder, fname, loc, date, stamp_id):
    stamp = (
        'Issue Location: ' + path + '\n' +
        'Affected Folder: ' + folder + '\n' +
        'Affected File: ' + fname + '\n' +
        'Affected Line of Code: ' + loc + '\n' +
        'Generated by Issue Tracker: ' + date + '\n' +
        'Stamp Id: ' + stamp_id + '\n' +
        '\n'
    )
    return stamp


# Given our issue, delete it's current stamp
def delete_stamp(issue):
    stamp = None
    return (issue, stamp)


# Define a method for setting our stamp attributes based on what associations are present
# in our issue. Return these to our create stamp method below so we can generate a stamp.
def set_association_atrs(issue):
    # If a folder association is present, set our attributes and leave file and loc as None
    if issue.associated_folder:
        if issue.associated_folder.path:
            full_path = str(issue.repository.name) + '/' + str(issue.associated_folder.path)
        else:
            full_path = str(issue.repository.name)
        folder_name = str(issue.associated_folder.name)
        file_name = 'None'
        loc = 'None'

        # If we have a file association, set its value and re-define path based on the file
        if issue.associated_file:
            issue.associated_folder = issue.associated_file.parent_folder
            full_path = str(issue.associated_file.repository.name) + '/' + str(issue.associated_file.path)
            file_name = str(issue.associated_file.name)
            
            # If we've associated our issue with a line of code, set its value for the stamp
            # based on its line number
            if issue.associated_loc:
                issue.associated_file = issue.associated_loc.repofile
                issue.associated_folder = issue.associated_file.parent_folder
                loc = str(issue.associated_loc.line_number)

    # Return our parameters so we can set the stamp in our create stamp method
    return (full_path, folder_name, file_name, loc)


# If we're adding associations to an issue that previously had none, set the stamp attributes
# and create it
def create_stamp(issue):
    stamp_id = str(1234567812345678)
    # Set the date for when the stamp was generated
    date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
    # Call our set attributes method to get the rest of the stamp parameters
    path, folder, fname, loc = set_association_atrs(issue)
    # Now set our stamp with the parameters
    stamp = set_stamp(path, folder, fname, loc, date, stamp_id)
    # Populate our model field with our new stamp we set in the set_stamp method
    issue.stamp = stamp
    return issue.stamp


# If we're changing existing associations on our Issue instance, first delete the
# old stamp, then create a new one
def update_stamp(issue):
    issue, issue.stamp = delete_stamp(issue)
    # body = create_stamp(issue, body=issue.body)
    stamp = create_stamp(issue)
    return (issue, stamp)


# Given the old associations and the issue itself, check if any associations changed,
# then update the stamp accordingly
def check_associations(old, issue):
    new = [issue.associated_folder, issue.associated_file, issue.associated_loc]
    # Check for changes
    if old != new:
        # Check if all the old values were empty and if all the new values will be empty
        old_none = all(atr is None for atr in old)
        new_none = all(atr is None for atr in new)

        # If we're adding an association when there were none before, call the create stamp method
        if old_none == True and new_none == False:
            print('create')
            issue.stamp = create_stamp(issue)
        
        # If we're updating existing associations, call our update stamp method
        elif old_none == False and new_none == False:
            print('update')
            issue, issue.stamp = update_stamp(issue)

        # If we're removing all associations, call our delete stamp method
        elif old_none == False and new_none == True:
            print('delete')
            issue, issue.stamp = delete_stamp(issue)
            return issue.stamp
    # Return our new issue stamp to Issue's save method so we can update the field
    return issue.stamp


# # Let's create unique slugs for each model object from the object name using itertools.
# # We'll also define a method for updating slugs if the name changes.
def generate_slug(instance, model):
    # Check which model we're using
    if hasattr(instance, 'name'):
        value = instance.name
        slug_value = slugify(value)
    else:
        value = instance.title
        slug_value = slugify(value).title()

    slug_candidate = slug_original = slug_value + '_' + str(1)
    # Count until we find an empty 'slot' for our slug
    for i in itertools.count(1):
        if not model.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = '{}_{}'.format(slug_value, str(i))
    # If we're creating the first object, set slug to default value above
    if i == 1:
        slug_new = slug_original
    # Otherwise, set it based on itertools.count()
    else:
        slug_new = slug_candidate
    # For larger sites we would want to define a max_length for slugs
    instance.slug = slug_new
    return instance.slug


# Define our Issue model for the database
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
    number = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length = 200, unique=True)
    stamp = models.TextField(null=True, blank=True, editable=False)

    # Foreign keys
    author = models.ForeignKey(
       Profile,
       max_length=100,
       on_delete=models.CASCADE,
       related_name='issue_author'
    )
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
    
    # Methods
    # Override the model's initialization method so we can check for changes in values
    # we want to save with custom methods
    def __init__(self, *args, **kwargs):
        super (Issue, self).__init__(*args, **kwargs)
        self.__original_title = self.title
        self.__original_associated_folder = self.associated_folder
        self.__original_associated_file = self.associated_file
        self.__original_associated_loc = self.associated_loc

    # Override the model's save method so we can include custom save methods
    def save(self, *args, **kwargs):
        # If we're creating the object for the first time, generate a slug
        if not self.pk:
            # self._get_slug()
            self.slug = generate_slug(self, Issue)
        # Else if we changed the name, generate a slug
        elif self.title != self.__original_title:
            # self._get_slug()
            self.slug = generate_slug(self, Issue)

        # If we're changing the associated files, folders or lines of codes, let's
        # update the body with our custom stamp methods defined above
        old = [self.__original_associated_folder, self.__original_associated_file, self.__original_associated_loc]
        self.stamp = check_associations(old, self)
        super().save(*args, **kwargs)
    
    # Built in redirect for create view
    def get_absolute_url(self):
        return reverse('issue-read', kwargs={'issue_slug': self.slug})

    # Define which attribute the issue will be listed by in the admin portion of the site
    def __str__(self):
        return self.title


#################################################################################################################################
# END
#################################################################################################################################
