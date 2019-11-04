from django.http import HttpResponse
from django.shortcuts import render
import requests
import sys

from subprocess import run,PIPE
def button(request):
	return render(request,'home.html')
	
def result(request):
	return render(request,'result.html')
