from repositories.models import LineOfCode
from django import forms
from django.forms import ModelForm
from . models import Issue
from repositories.models import RepoFolder, RepoFile


class IssueSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Search title, body, date, etc.', 'class': 'issue-search'}
        ))

class IssueEntryForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'title', 'body', 'repository', 'associated_folder', 
            'associated_file', 'associated_loc'
            ]

    def __init__(self, *args, **kwargs):
        super(IssueEntryForm, self).__init__(*args, **kwargs)

        self.fields['associated_folder'].label = 'Folder'
        self.fields['associated_file'].label = 'File'
        self.fields['associated_loc'].label = 'Line of Code'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'issue-form-field'

        for key, field in self.fields.items():
            if key.startswith('associated_'):
                field.widget.attrs = {'class': 'associate-field'}

        if kwargs['instance']:
            repo_id = kwargs['instance'].repository.id
            self.fields['associated_folder'].queryset = RepoFolder.objects.filter(
                    repository=repo_id).order_by('name')

            self.fields['repository'].widget.attrs['disabled'] = True
            self.fields['repository'].required = False

            if kwargs['instance'].associated_folder:
                folder_id = kwargs['instance'].associated_folder.id
                self.fields['associated_file'].queryset = RepoFile.objects.filter(
                        parent_folder=folder_id).order_by('name')
            else:
                self.fields['associated_file'].queryset = RepoFile.objects.none()
            
            if kwargs['instance'].associated_file:
                file_id = kwargs['instance'].associated_file.id
                self.fields['associated_loc'].queryset = LineOfCode.objects.filter(
                        repofile=file_id).order_by('line_number')
            else:
                self.fields['associated_loc'].queryset = LineOfCode.objects.none()

        if 'repository' in self.data:
            try:
                repo_id = int(self.data.get('repository'))
                self.fields['associated_folder'].queryset = RepoFolder.objects.filter(
                    repository=repo_id).order_by('name')
            except (ValueError, TypeError):
                pass
        
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
    
    def clean_repository(self):
        if self.instance and self.instance.pk:
            return self.instance.repository
        else:
            return self.cleaned_data['repository']


class OpenCloseIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['state']
        widgets = {'state': forms.HiddenInput()}
