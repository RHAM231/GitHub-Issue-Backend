from django import forms


# Instantiate our navbar search form and make it's single field not required
class MasterSearchForm(forms.Form):
    master_search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Issues, Projects, Folders, etc.', 'class': 'ms-form-style'}
        )
    )
