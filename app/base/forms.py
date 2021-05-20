from django import forms


class MasterSearchForm(forms.Form):
    master_search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Issues, Projects, Folders, etc.', 'class': 'ms-form-style'}
        )
    )
