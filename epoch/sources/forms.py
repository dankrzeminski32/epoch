from django import forms


class CustomSourceForm(forms.Form):
    custom_source = forms.URLField(label="Source URL", max_length=200)
