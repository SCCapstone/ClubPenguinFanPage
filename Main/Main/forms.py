from django import forms

class InputTextForm(forms.Form):
    analysis_text = forms.CharField(widget= forms.Textarea, label="Input Text", max_length=1000)
    stop_words = forms.CharField(widget= forms.Textarea, label="Stop Words", max_length=200)