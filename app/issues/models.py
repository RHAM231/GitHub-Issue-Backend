import datetime
import itertools
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db import models
from users.models import CustomUser


class Issue(models.Model):
    STATE_CHOICES = (
        ('open', 'open'),
        ('closed', 'closed'),
    )

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=6, choices = STATE_CHOICES, default='open')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False)
    updated_at = models.DateTimeField(auto_now=False)
    closded_at = models.DateTimeField(auto_now=False) 
    number = models.IntegerField()
    
    # Let's create unique slugs for each issue from the issue name and primary key
    # We'll also define a method for updating slugs if the name changes
    def _generate_slug(self):
        # For larger sites we would want to define a max_length for slugs
        value = self.name
        slug_candidate = slug_original = slugify(value).upper() + '_' str(1)
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
        self.__origianl_name = self.name

    # Override the model's save method so we can save and update slugs automatically
    def save(self, *args, **kwargs):
        # If we're creating the issue for the first time, generate a slug
        if not self.pk:
            self._generate_slug()
        # Else if we changed the name, generate a slug
        elif self.name != self.__original_name:
            self._generate_slug()
        super().save(*args, **kwargs)
    
    # Built in redirect for create view
    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'issue_slug': self.slug})

    # Define which attribute the issue will be listed by in the admin portion of the site
    def __str__(self):
        return self.name
