from repositories.models import LineOfCode
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


# Issue form for creating and updating issues
class IssueEntryForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'title', 'body', 'repository', 'associated_folder', 
            'associated_file', 'associated_loc'
            ]

    # Override the form's init method to set labels, classes, and populate dropdown data
    def __init__(self, *args, **kwargs):
        super(IssueEntryForm, self).__init__(*args, **kwargs)

        # Set custom labels on our association fields
        self.fields['associated_folder'].label = 'Folder'
        self.fields['associated_file'].label = 'File'
        self.fields['associated_loc'].label = 'Line of Code'

        # Set a class for all our fields to make CSS cleaner
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'issue-form-field'

        # Set a special class for our association fields so we can style them differently
        for key, field in self.fields.items():
            if key.startswith('associated_'):
                field.widget.attrs = {'class': 'associate-field'}

        # If the form already has data when loaded (update/edit) set the querysets
        # for the file and line of code fields based on the ids of the folder and
        # file fields
        # Check for existing data
        if kwargs['instance']:
            # Check for folder data
            if kwargs['instance'].associated_folder:
                # Get our folder id
                folder_id = kwargs['instance'].associated_folder.id
                # Set the file queryset for the dropdown
                self.fields['associated_file'].queryset = RepoFile.objects.filter(
                        parent_folder=folder_id).order_by('name')
            # Otherwise start the value as empty
            else:
                self.fields['associated_file'].queryset = RepoFile.objects.none()
            
            # Repeat for lines of code
            if kwargs['instance'].associated_file:
                file_id = kwargs['instance'].associated_file.id
                self.fields['associated_loc'].queryset = LineOfCode.objects.filter(
                        repofile=file_id).order_by('line_number')
            else:
                self.fields['associated_loc'].queryset = LineOfCode.objects.none()

        # If folder or file were selected in the form submit, set the querysets for
        # file and line of code to match, since it may have changed on the frontend
        # from AJAX updates
        if 'associated_folder' in self.data:
            try:
                folder_id = int(self.data.get('associated_folder'))
                self.fields['associated_file'].queryset = RepoFile.objects.filter(
                    parent_folder=folder_id).order_by('name')
            except (ValueError, TypeError):
                pass
        
        if 'associated_file' in self.data:
            try:
                file_id = int(self.data.get('associated_file'))
                self.fields['associated_loc'].queryset = LineOfCode.objects.filter(
                    repofile=file_id).order_by('line_number')
            except (ValueError, TypeError):
                pass


# Form for changing the state of an issue. Used on the issue detail page
class OpenCloseIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['state']
        widgets = {'state': forms.HiddenInput()}
