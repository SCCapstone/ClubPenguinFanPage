from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hellooooooooo, you've reached the textanalysis login page")
