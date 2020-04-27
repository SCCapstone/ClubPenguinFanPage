from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, update_session_auth_hash, REDIRECT_FIELD_NAME
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.db import models
from django.contrib.auth import login as auth_login

from .forms import LoginForm

#This is the reset password view
def change_password(request):
	if request.method == 'POST':
		#Use the default Password Change Form that comes with Django import
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request,user)
			#This message would appear however it redirects before it is shown
			messages.success(request, 'Your password was successfully changed')
			return redirect('/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'registration/change_password.html',{ 'form': form})

#This is the login view
def login(request):
	#Use the LoginForm class that was made in forms.py
	form = LoginForm(request.POST)
	if request.POST and form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		rememberMe = form.cleaned_data['rememberMe']
		user = form.login(request)
		if user:
			#A tried method to implementing remember me functionality
			if not request.POST.get('rememberMe',None):
				request.session.set_expiry(0)
			else:
				#represents 2 weeks in seconds
				request.session.set_expiry(1209600)
			auth_login(request, user)
			#redirect to home page
			return redirect('')
	return render(request, 'registration/login.html', {'form': form})

class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'
	


# Create your views here.
	
		
