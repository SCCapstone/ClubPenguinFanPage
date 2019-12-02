from django import forms

class InputTextForm(forms.Form):
    input_text = forms.CharField(label="Input Text", max_length=500)

