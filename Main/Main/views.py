from django.shortcuts import render, get_object_or_404, redirect, render_to_response
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from .forms import createProjectForm
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.apps import apps


def button(request):
    return render(request, 'home.html')


# runs tf-idf algorithm, returns ranked list 
def tfidf(text):
    tokens = []
    s = ''
    for elem in text:
        tokens.append(elem.lower().translate(string.punctuation))

    vectorizer = TfidfVectorizer(stop_words='english')
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
    return ranking[['feat','rank']].to_html(index=False)
    

def result(request):
    text = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
    newtext = tfidf(text)
    textout = '<br>'.join(text)
    return render(request, 'result.html', {'text': textout, 'newtext': newtext})


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
        return redirect("/recentlyused")
    else:
        return render(request, 'createProject.html')
    
def recentlyused(request, new_context={}):
        Project = apps.get_model('accounts', 'Project')
        Document = apps.get_model('accounts', 'Document')
        user = request.user
        project_list=Project.objects.filter(owner=user.id)
        context = {
            'proj_list': project_list,
        }
        context.update(context)
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