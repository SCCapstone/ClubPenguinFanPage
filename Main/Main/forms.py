from django import forms

class InputTextForm(forms.Form):
    analysis_text = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%;"}), label="Input Text", max_length=1000)
    stop_words = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'style': "width:100%;"}), label="Stop Words", max_length=200)