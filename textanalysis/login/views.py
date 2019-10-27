from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, you've reached the textanalysis login page")