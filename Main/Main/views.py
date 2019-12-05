from django.http import HttpResponse
from django.shortcuts import render
import sys
import nltk, string, os, pandas as pd
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from .forms import InputTextForm
#from .forms import UploadFileForm
from .functions.functions import handle_uploaded_file 

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
    txt = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
    newtext = tfidf(txt)
    textout = '<br>'.join(txt)
    return render(request, 'result.html', {'text': textout, 'newtext': newtext})
