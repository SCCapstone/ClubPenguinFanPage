from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
import string
from django.http import HttpResponse
from django.apps import apps
import sys, os
import nltk, string, os, pandas as pd
import numpy as np
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from datetime import date 
from .forms import InputTextForm
#from .forms import UploadFileForm
from .functions.functions import handle_uploaded_file 
import mimetypes

from subprocess import run,PIPE
# def button(request):
#     return render(request, 'home.html')

def get_input_text(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InputTextForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/result/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = InputTextForm()
    return render(request, 'home.html', {'form': form})

def button(request):
    return render(request, 'home.html')


# runs tf-idf algorithm, returns ranked list 
def tfidf(txt):
    tokens = []
    s = ''
    for elem in txt:
        tokens.append(elem.lower().translate(string.punctuation))
    user_stopwords = ['man']
    stopwords = text.ENGLISH_STOP_WORDS.union(user_stopwords)
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    vectors = vectorizer.fit_transform(tokens)
    feature_names = vectorizer.get_feature_names()

    # sum tfidf frequency of each term through documents
    sums = vectors.sum(axis=0)

    # connecting term to its sums frequency
    data = []
    for col, feat in enumerate(feature_names):
        data.append( (feat, sums[0,col] ))

    ranking = pd.DataFrame(data, columns=['feat','rank'])
    ranking = ranking.sort_values('rank', ascending=False)
    return ranking[['feat','rank']], ranking[['feat','rank']].to_html(index=False)
    

def result(request):
    txt = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
    textout = '<br>'.join(txt)
    filename = 'output.txt'
    try:
        os.remove(filename)
    except:
        print('file not found exception')
    tfidf(txt)[0].to_csv(filename, header=None, index=None, sep=' ', mode='a')
    newtext = tfidf(txt)[1]
    textout = '<br>'.join(txt)
    return render(request, 'result.html', {'text': textout, 'newtext': newtext})


def download_file(request):
    fl_path = 'output.txt'
    filename = 'output.txt'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def createProject(request):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    if request.method == 'POST':
        text = request.POST.get("textInput")
        title = request.POST.get("titleInput")
        user = request.user
        
        p = Project(owner=user, title=title)
        p.save()
        
        d = Document(project=p, text=text)
        d.save()
        
        #might break here because p is only saved right before making document go to it
        project_list=Project.objects.filter(owner=user.id)
        context = {
            'proj_list': project_list,
        }
        return redirect("recentlyused")
    else:
        return render(request, 'createProject.html')
    
def recentlyused(request):
        Project = apps.get_model('accounts', 'Project')
        Document = apps.get_model('accounts', 'Document')
        user = request.user
        project_list=Project.objects.filter(owner=user.id)
        context = {
            'proj_list': project_list,
        }
        return render(request,"recentlyused.html",context=context)

#def newProject(self, request):
    #form = createProjectForm()
    #return render(request, 'createProject.html', {'form': form})

def newProject(self, request):
    if request.method == 'POST':
        if request.POST.get('docText'):
            print(request.POST.get('textInput'))
    return render(request, 'createProject.html')
    
def project_detail(request, project_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    documents = Document.objects.filter(project=project_id)
    proj = Project.objects.get(pk=project_id)
    title = proj.title
    context= {
        'doc_list': documents,
        'project': proj,
        'title': title,
    }
    return render(request, "projectview.html", context=context)
    
#DELETE ALL PROJECTS AND DOCUMENTS
def delete_all_projects(self):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    Document.objects.all().delete()
    Project.objects.all().delete()
    print("All project and document objects have been deleted")
    return redirect("/")
