from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import nltk, string, sys, os, pandas as pd
import numpy as np
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from datetime import date 
#WE NEED TO ABSOLUTE PATH THESE IMPORTS IF THEY'RE NEEDED
    #from .forms import InputTextForm
    #from .forms import UploadFileForm
    #from .functions.functions import handle_uploaded_file 
import mimetypes

from subprocess import run,PIPE
# def button(request):
#     return render(request, 'home.html')

def home(request):
    return render(request, "home.html")

def button(request):
    return render(request, 'home.html')

# runs tf-idf algorithm, returns ranked list 
def tfidf(txt, sw):
    tokens = []
    s = ''
    for elem in txt:
        tokens.append(elem.lower().translate(string.punctuation))
    #parse this
    user_stopwords = sw_clean(sw)
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
    return ranking[['feat','rank']][0:15], ranking[['feat','rank']][0:15].to_html(index=False)
    

def result(request):
    if request.method == 'POST':
        upfile = request.POST.get("uploadfile")
        txt = request.POST.get("input_text")
        sw = request.POST.get("stopwords")
        stopwords = text.ENGLISH_STOP_WORDS.union(sw)
        if txt is '':
            txt = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
            textout = '<br>'.join(txt)
            filename = 'output-' + str(date.today()) + '.txt'
            tfidf(txt, sw)[0].to_csv(filename, header=None, index=None, sep=' ', mode='a')
            newtext = tfidf(txt, sw)[1]
            textout = '<br>'.join(txt) 
            return render(request, 'result.html', {'text': textout, 'newtext': newtext})
    else:
        txt = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
    filename = 'output.txt'
    try:
        os.remove(filename)
    except:
        print('file not found exception')
    txt = clean_up(txt)
    tfidf(txt, sw)[0].to_csv(filename, header=None, index=None, sep=' ', mode='a')
    newtext = tfidf(txt, sw)[1]
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
    
#ADD DOCUMENT TO PROJECDT
def add_document(request, project_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    new_doc = request.POST.get('textInput')
    
    proj = Project.objects.get(pk=project_id)
        
    d = Document(project=proj, text=new_doc)
    d.save()
    
    documents = Document.objects.filter(project=project_id)
    title = proj.title
    context= {
        'doc_list': documents,
        'project': proj,
        'title': title,
    }
    return redirect("recentlyused")

#other methods for other stuff
def clean_up(txt):
    clean_text = txt
    clean_list = clean_text.split("\r\n")
    num_of_doc = len(clean_list)
    print(clean_list)
    return clean_list
    
def sw_clean(sw):
    clean_sw = sw
    sw_list = clean_sw.split(" ")
    return sw_list

#def read_file_text(file):

#things to do (Ainsley)
#-style project creation/recently used
#-fonts of tfidf results and input at home
#-upload file
