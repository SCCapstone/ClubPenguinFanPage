from django import forms

class InputTextForm(forms.Form):
    file      = forms.FileField(required=False) # for creating file input
    analysis_text = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%;"}), label="Input Text", max_length=1000, required=False)
    stop_words = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'style': "width:100%;"}), label="Stop Words", max_length=200, required=False)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class createProjectForm(forms.Form):
    proj = forms.Textarea()
