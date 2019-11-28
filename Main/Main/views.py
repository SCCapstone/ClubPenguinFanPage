from django.http import HttpResponse
from django.shortcuts import render
import sys
import nltk, string, os, pandas as pd
import string
import numpy as np
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

from subprocess import run,PIPE
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
    return ranking[['feat','rank']].to_html(index=False)
    

def result(request):
    txt = ['the man went out for a walk',
            'the children sat around the fire',
            'fires are burning down homes',
            'i shall walk to the grocery store tomorrow']
    newtext = tfidf(txt)
    textout = '<br>'.join(txt)
    return render(request, 'result.html', {'text': textout, 'newtext': newtext})
