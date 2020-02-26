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
from collections import defaultdict
from datetime import date 
#WE NEED TO ABSOLUTE PATH THESE IMPORTS IF THEY'RE NEEDED
    #from .forms import InputTextForm
    #from .forms import UploadFileForm
    #from .functions.functions import handle_uploaded_file 
import mimetypes
from gensim import corpora
from gensim import models
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

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
    #user_stopwords = sw_clean(sw)
    vectorizer = TfidfVectorizer(stop_words=sw)
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
    
def lda(txt, sw, noOfTopics):
    outputstring = ""
    documents = []
    ignoreList = []
    punctList = []
    punctList = [".", ",", "?", "!", ";", ":", "\"", "'",
                "…", "–", "--", "[","]", "’"]
    # user inputted stopwords go here
    stop_words = ['for', 'a', 'of', 'the', 'and', 'to', 'in']
    ignoreList += text.ENGLISH_STOP_WORDS.union(stop_words)
    s = ""
    # a bit would be considered each paragraph/document, a token would be
    # considered a word in that paragraph
    for bit in txt:
        s = ""
        for token in bit.split():
            for i in range(0, len(token)):
                # checks if any of the characters in the word are punctuation,
                # removes it if so
                if(token[i] in punctList):
                    token = token.replace(token[i], ' ')
            token = token.replace(" ", "")
            if token.lower() not in ignoreList:
                s += token + " "
        documents.append(s)
    stoplist = make_sw_list(sw)
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]
    # remove words that appear only once
    frequency = defaultdict(int)
    for t in texts:
        for token in t:
            frequency[token] += 1

    texts = [[token for token in t if frequency[token] > 1]
              for t in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(t) for t in texts]

    tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
    corpus_tfidf = tfidf[corpus]

    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=noOfTopics)  # initialize an LDA transformation
    corpus_lda = lda[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    f = open("output.txt", "w")
    s = ''
    noOfTopics = int(noOfTopics)
    for i in range(noOfTopics):
        s = "Topic " + str(i+1) + "\n"
        f.write(s)
        outputstring = outputstring + s + "\n"
        # topic = lsi.print_topic(i, x)
        # where x = number of words per topic if desired
        topic = lda.print_topic(i)
        for t in topic.split('+'):
            t = t.replace(" ", "").replace('*', " ")
            f.write(t + "\n")
            outputstring = outputstring + t + "\n"
    f.close()
    return outputstring

#treating each letter as a document, but STOPWORDS WORKING
def pos(txt, sw):
    cnt = 1
    outputstring = ""
    for doc in txt:
        tokenized = sent_tokenize(doc)
        stop_words = make_sw_list(sw)
        if tokenized != []:
            print("Document " + str(cnt))
            outputstring = outputstring + "Document" + str(cnt) + "\n"
            for i in tokenized:
                wordsList = nltk.word_tokenize(i)
                wordsList = [w for w in wordsList if not w in stop_words]
                tagged = nltk.pos_tag(wordsList)
                print(tagged)
                for tag in tagged:
                    outputstring = outputstring + tag[0] + ": " + tag[1] + "\n"
            cnt += 1
    return outputstring
    

#COMPLICATED WORK HERE!!!!!!!
def result(request):
    if request.method == 'POST':
        algorithm = request.POST.get("algorithm")
        if len(request.FILES) != 0:
            file = request.FILES['fileInput']
            user = request.user
            txt = file.read()
            txt=str(txt,'utf-8')
        input_text = request.POST.get("textInput")
        if input_text != '':
            txt = input_text
        sw = request.POST.get("sws")
        num_of_topics = request.POST.get("ldarange")
        if algorithm == 'tfidf':
            textout, newtext = tfidfprocess(txt, sw)
            context = {
                'text': textout, 
                'newtext': newtext, 
                'algorithm': 'tfidf'
            }
            return render(request, 'result.html', context = context)
        if algorithm == 'pos': 
           outputstring = posprocess(txt, sw)
           context = {
               'text': txt,
               'outputstring': outputstring,
               'algorithm': 'pos'
           }
           return render(request, 'result.html', context= context)
        if algorithm == 'lda':
            outputstring = ldaprocess(txt, sw, num_of_topics)
            context = {
                'text': txt,
                'outputstring': outputstring,
                'algorithm': 'lda'
            }
            return render(request, 'result.html', context=context)
    else:
        txt = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
    return render(request, 'result.html')

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
        
        if len(request.FILES) != 0:
            file = request.FILES['fileInput']
            user = request.user
            
            #parse txt from files
            
            txt = file.read()
            txt=str(txt,'utf-8')
            
            p = Project(owner=user, title=title)
            p.save()
            
            d = Document(project=p, text=txt)
            d.save()
            
            project_list=Project.objects.filter(owner=user.id)
            context = {
                'proj_list': project_list,
            }
            return redirect("recentlyused")
        elif text is not None:
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
    proj = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        text = request.POST.get("textInput")
        if len(request.FILES) != 0:
            file = request.FILES['fileInput']
            user = request.user
            
            #parse txt from files
            
            txt = file.read()
            txt=str(txt,'utf-8')
            
            d=Document(project=proj, text=txt)
            d.save()
        elif text is not None:
            d = Document(project=proj, text=text)
            d.save()

    return redirect("project_detail", project_id=project_id)

def analyze_doc_tfidf(request, document_id):
    Document = apps.get_model('accounts', 'Document')
    doc = Document.objects.get(pk=document_id)
    txt = doc.text
    sw = request.POST.get('sws')
    textout, newtext = tfidfprocess(txt, sw)
    context = {
        'text': textout, 
        'newtext': newtext, 
        'algorithm': 'tfidf'
    }
    return render(request, 'result.html', context = context)
    
    
#other methods for other stuff
def clean_up(txt):
    clean_text = txt
    clean_list = clean_text.split("\r\n")
    num_of_doc = len(clean_list)
    return clean_list
    
def sw_clean(sw):
    clean_sw = sw
    sw_list = clean_sw.split(" ")
    return sw_list
    
def make_sw_list(sw):
    user_stopwords = sw_clean(sw)
    return text.ENGLISH_STOP_WORDS.union(sw)
    
def tfidfprocess(txt, sw):
    txt = clean_up(txt)
    sws = make_sw_list(sw)
    newtext = tfidf(txt, sws)[1]
    textout = '<br>'.join(txt)
    return textout, newtext
   
#needs work 
def posprocess(txt, sw):
    txt = clean_up(txt)
    outputstring = pos(txt, sw)
    return outputstring
    
def ldaprocess(txt, sw, numberoftopics):
    txt = clean_up(txt)
    outputstring = lda(txt, sw, numberoftopics)
    return outputstring
    

#def read_file_text(file):

#things to do (Ainsley)
#-for upload file, error cleaning
#-for sending project document to tf-idf, not printing


#ERRORS TO CREATE MESSAGES FOR:
#-in case all words are stopwords
#-in case blank text submitted/nofile submitted