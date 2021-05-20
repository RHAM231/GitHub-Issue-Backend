from django import forms


REPO_CHOICES = [
    ('Sandbox-Import', 'Sandbox-Import'),
    ('IssueTrackerSandbox', 'IssueTrackerSandbox'),
]


class ImportRepoForm(forms.Form):
    repository = forms.CharField(
        required=False, 
        widget=forms.Select(
            attrs={'class':'issue-form-field'},
            choices=REPO_CHOICES))