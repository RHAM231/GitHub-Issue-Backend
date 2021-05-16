from django import forms


# Define the repository choices for the form below
REPO_CHOICES = [
    ('Sandbox-Import', 'Sandbox-Import'),
    ('IssueTrackerSandbox', 'IssueTrackerSandbox'),
]


# Define a select field import form for repositories so we can reuse our view
# and template when importing repos
class ImportRepoForm(forms.Form):
    repository = forms.CharField(
        required=False, 
        widget=forms.Select(
            attrs={'class':'issue-form-field'},
            choices=REPO_CHOICES))