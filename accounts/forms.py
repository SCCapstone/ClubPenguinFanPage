from django import forms
from django.contrib.auth.forms import AuthenticationForm

#This is the Login form used in accounts/views.py
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    rememberMe = forms.BooleanField()
	
			
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
		
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
       # if self.cleaned_data.get('rememberMe'):
       #     self.request.session.set_expiry(0)
       # else:
       #     self.request.session.set_expiry(1209600)
        user = authenticate(username=username, password=password)
        return user