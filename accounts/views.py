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

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request,user)
			messages.success(request, 'Your password was successfully changed')
			return redirect('/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'registration/change_password.html',{ 'form': form})

class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'
	


# Create your views here.
	
		
