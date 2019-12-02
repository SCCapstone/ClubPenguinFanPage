from django import forms

class InputTextForm(forms.Form):
    analysis_text = forms.CharField(label="Input Text", max_length=1000)
    stop_words = forms.CharField(label="Stop Words", max_length=200)


