from django import forms


class createProjectForm(forms.Form):
    proj = forms.Textarea()
