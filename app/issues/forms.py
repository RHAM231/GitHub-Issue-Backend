from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Issue
from repositories.models import RepoFolder, RepoFile


FILTER_CHOICES = [
    # ('title', 'Filters'),
    ('Open', 'Open'),
    ('Closed', 'Closed'),
    ('your_issues', 'Your Issues'),
]

OPEN_CLOSED_CHOICES = [
    ('open', 'Open'),
    ('closed', 'Closed'),
]

AUTHOR_CHOICES = [
    ('title', 'Author'),
    ('project1', 'Project1'),
]

PROJECT_CHOICES = [
    ('title', 'Projects'),
    ('project1', 'Project1'),
]

FOLDER_CHOICES = [
    ('title', 'Folders'),
    ('folder1', 'Folder1'),
]

FILE_CHOICES = [
    ('title', 'Files'),
    ('file1', 'File1'),
]

SORT_CHOICES = [
    ('title', 'Sort'),
    ('newest', 'Newest'),
    ('oldest', 'Oldest'),
    ('recently_updated', 'Recently Updated'),
    ('least_recently_updated', 'Least Recently Updated'),
]


class IssueSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Search title, body, date, etc.', 'class': 'issue-search'}
        ))
    open_filter = forms.CharField(
        required=False,
    )
    closed_filter = forms.CharField(
        required=False,
    )


class IssueStateFilterForm(forms.Form):
    btn = forms.CharField()


class IssueEntryForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'title', 'body', 'repository', 'associated_folder', 
            'associated_file', 'associated_loc'
            ]

    def __init__(self, *args, **kwargs):
        super(IssueEntryForm, self).__init__(*args, **kwargs)

        self.fields['associated_file'].queryset = RepoFolder.objects.none()

        self.fields['associated_folder'].label = 'Folder'
        self.fields['associated_file'].label = 'File'
        self.fields['associated_loc'].label = 'Line of Code'


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'issue-form-field'

        for key, field in self.fields.items():
            if key.startswith('associated_'):
                field.widget.attrs = {'class': 'associate-field'}


class OpenCloseIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['state']
        widgets = {'state': forms.HiddenInput()}
