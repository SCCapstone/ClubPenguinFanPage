from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import sys
import nltk, string, os, pandas as pd
import string
import numpy as np
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from datetime import date 
from .forms import InputTextForm
#from .forms import UploadFileForm
from .functions.functions import handle_uploaded_file 

from subprocess import run,PIPE
# def button(request):
#     return render(request, 'home.html')

def home(request):
    return render(request, "home.html")

'''
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
'''

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
    textout = '<br>'.join(txt)
    filename = 'output-' + str(date.today()) + '.txt'
    txt = clean_up(txt)
    tfidf(txt, sw)[0].to_csv(filename, header=None, index=None, sep=' ', mode='a')
    newtext = tfidf(txt, sw)[1]
    textout = '<br>'.join(txt)
    return render(request, 'result.html', {'text': textout, 'newtext': newtext})


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

#def read_file_text(file):

#things to do (Ainsley)
#-style project creation/recently used
#-fonts of tfidf results and input at home
#-upload file