from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import nltk, string, sys, os, re, glob, pandas as pd
import numpy as np
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
from datetime import date
from colour import Color
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
def tfidf(txt, present_txt, sw):
    print(present_txt)
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

    top15 = []
    top15_freqs = []
    t = ranking.iloc[0:15].values.tolist()
    top15 = {}
    for item in t:
        top15.update({item[0]: item[1]})
    top15_words = ranking.iloc[:,0][0:15].values.tolist()
    top15_freqs = ranking.iloc[:,1][0:15].values.tolist()
    top15_freqs = list(set(top15_freqs))
    top15_freqs = [float(i) for i in top15_freqs]
    top15_freqs_sort = sorted(top15_freqs)

    col1 = Color("#DFFDFE")
    colors = list(col1.range_to(Color("#26267A"),len(top15_freqs_sort)))
    colors = [str(c) for c in colors]
    #print(colors)

    txt_hl = ''
    outputstring = ''
    for para in present_txt:
        for word in para.split():
            if word.startswith('<strong>'):
                word = '<br><br>' + word
            if word.endswith('</strong>'):
                word = word + '<br>'
            clean_word = word.translate(str.maketrans('', '', string.punctuation)).lower()
            if clean_word in top15_words:
                for freq in top15_freqs_sort:
                    if top15[clean_word] == freq:
                        if top15_freqs_sort.index(freq) >= len(colors) / 2:
                            word = '<span style="color:white;background-color:' + colors[top15_freqs_sort.index(freq)] + '">' + word + '</span>'
                        else:
                            word = '<span style="background-color:' + colors[top15_freqs_sort.index(freq)] + '">' + word + '</span>'
            txt_hl += word + ' '
            outputstring += "<table style='padding:15px;margin-left:auto;margin-right:auto;'>"
        txt_hl += '<br>'

    top15 = ranking[['feat','rank']][0:15]
    for i in range(len(top15)):
        if top15_freqs_sort.index(top15.iloc[i,1]) >= len(colors) / 2:
            outputstring += '<tr> <td style="color:white;background-color:' + colors[top15_freqs_sort.index(top15.iloc[i,1])] + '">' + top15.iloc[i,0] + '</td>'
            outputstring += '<td style="color:white;background-color:' + colors[top15_freqs_sort.index(top15.iloc[i,1])] + '">' +str(round(top15.iloc[i,1],4)) + '</td></tr>'
        else:
            outputstring += '<tr> <td style="background-color:' + colors[top15_freqs_sort.index(top15.iloc[i,1])] + '">' + top15.iloc[i,0] + '</td>'
            outputstring += '<td style="background-color:' + colors[top15_freqs_sort.index(top15.iloc[i,1])] + '">' +str(round(top15.iloc[i,1],4)) + '</td></tr>'
    outputstring += "</table>"

    return ranking[['feat','rank']][0:15], outputstring, txt_hl

def lda(txt, present_txt, sw, noOfTopics):
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
    noOfTopics = int(noOfTopics)

    col1 = Color("#C5E9EE")
    colors = list(col1.range_to(Color("#709FCF"),noOfTopics))
    colors = [str(c) for c in colors]

    topic_contents = []
    file_string = ""
    for i in range(noOfTopics):
        s = '<span style="background-color:' + colors[i] + '">' + "\nTopic " + str(i+1) + "\n"+ '</span>'
        file_string += "\nTopic " + str(i+1) + "\n"
        outputstring = outputstring + s + "\n"
        # topic = lsi.print_topic(i, x)
        # where x = number of words per topic if desired
        words = []
        topic = lda.print_topic(i)
        outputstring += "<table style='padding:15px;margin-left:auto;margin-right:auto;'>"
        for t in topic.split('+'):
            t = t.replace(" ", "").replace('*', " ")
            w = (re.sub(r"[0-9.\"]+", '', t)).strip(' ')
            words.append(w)
            outputstring += "<tr> <td>" + t.split(" ")[1].strip('"') + "<td>" + t.split(" ")[0] + "</tr>"
            file_string += t + "\n"
        topic_contents.append(words)
        outputstring += "</table>"

    txt_hl = ''
    for para in present_txt:
        for word in para.split():
            if word.startswith('<strong>'):
                word = '<br><br>' + word
            if word.endswith('</strong>'):
                word = word + '<br>'
            clean_word = word.translate(str.maketrans('', '', string.punctuation)).lower()
            for topic in topic_contents:
                if clean_word in topic:
                    word = '<span style="background-color:' + colors[topic_contents.index(topic)] + '">' + word + '</span>'
            txt_hl += word + ' '
    return outputstring, file_string, txt_hl

def pos(txt, present_txt, sw):
    cnt = 1
    outputstring = ""
    file_string = ''
    tags_dict = {
    "CC": "coordinating conjunction",
    "CD": "cardinal digit",
    "DT": "determiner",
    "EX": "existential there",
    "FW": "foreign word",
    "IN": "preposition/subordinating conjunction",
    "JJ": "adjective",
    "JJR": "adjective, comparative",
    "JJS": "adjective, superlative",
    "LS": "list marker",
    "MD": "modal",
    "NN": "noun, singular",
    "NNS": "noun plural",
    "NNP": "proper noun, singular",
    "NNPS": "proper noun, plural",
    "PDT": "predeterminer",
    "POS": "possessive ending",
    "PRP": "personal pronoun",
    "PRP$": "possessive pronoun",
    "RB": "adverb",
    "RBR": "adverb, comparative",
    "RBS": "adverb, superlative",
    "RP": "particle",
    "TO": "to",
    "UH": "interjection",
    "VB": "verb, base form",
    "VBD": "verb, past tense",
    "VBG": "verb, gerund/present participle",
    "VBN": "verb, past participle",
    "VBP": "verb, present tense",
    "VBZ": "verb, third person",
    "WDT": "wh-determiner",
    "WP": "wh-pronoun",
    "WP$": "possessive wh-pronoun",
    "WRB": "wh-abverb",
    ",":"comma",
    ".":"period",
    "''": "quotation marks",
    "``": "line break",
    "(": "open parenthesis",
    ")": "closed parenthesis",
    ":": "colon",
    ";": "semi-colon",
    "?": "question mark",
    "!": "exclamation mark"
    }

    col1 = Color("#DFFDFE")
    colors = list(col1.range_to(Color("#26267A"),4))
    colors = [str(c) for c in colors]
    #print(colors)

    doc = ''
    for t in txt:
        if t != '':
            doc += t
    tokenized = sent_tokenize(doc)
    stop_words = make_sw_list(sw)
    d = defaultdict(int)
    output_string = "The highlighting denotes <span style=background-color:" + colors[0] + ">nouns</span>, "
    output_string += "<span style=background-color:" + colors[1] + ">verbs</span>, "
    output_string += "<span style=color:white;background-color:" + colors[2] + ">adjectives</span>, and "
    output_string += "<span style=color:white;background-color:" + colors[3] + ">adverbs</span>, respectively."
    output_string += "<table style='margin-left:auto;margin-right:auto;'>"
    txt_hl = present_txt

    for i in tokenized:
        wordsList = nltk.word_tokenize(i)
        wordsList = [w for w in wordsList if not w in stop_words]
        tagged = nltk.pos_tag(wordsList)
        for tag in tagged:
                d[tag[1]] += 1
                if tag[0].lower() not in stop_words:
                    if tag[1].startswith('N'):
                        s = '<span style="background-color:' + colors[0] + '">' + tag[0] + '</span>'
                        txt_hl = re.sub(r'\b'+tag[0]+r'\b', s, txt_hl)
                    elif tag[1].startswith('V'):
                        s = '<span style="background-color:' + colors[1] + '">' + tag[0] + '</span>'
                        txt_hl = re.sub(r'\b'+tag[0]+r'\b', s, txt_hl)
                    elif tag[1].startswith('J'):
                        s = '<span style="color:white;background-color:' + colors[2] + '">' + tag[0] + '</span>'
                        txt_hl = re.sub(r'\b'+tag[0]+r'\b', s, txt_hl)
                    elif tag[1].startswith('R'):
                        s = '<span style="color:white;background-color:' + colors[3] + '">' + tag[0] + '</span>'
                        txt_hl = re.sub(r'\b'+tag[0]+r'\b', s, txt_hl)
                    file_string += tag[0] + "_" + tag[1] + "\n"

    if d != {}:
        data = []
        for tag in d:
            data.append( ((tag, d.get(tag))) )

        counts = pd.DataFrame(data, columns=['pos','cnt'])
        df = counts.sort_values('cnt', ascending=False)
        sort = df.values.tolist()
        for tag_info in sort:
            if tag_info[0] in tags_dict:
                if tag_info[0].startswith('N'):
                    fmt_tag = '<td style="background-color:' + colors[0] + '">' + tags_dict[tag_info[0]] + '</td>'
                elif tag_info[0].startswith('V'):
                    fmt_tag = '<td style="background-color:' + colors[1] + '">' + tags_dict[tag_info[0]] + '</td>'
                elif tag_info[0].startswith('J'):
                    fmt_tag = '<td style="color:white;background-color:' + colors[2] + '">' + tags_dict[tag_info[0]] + '</td>'
                elif tag_info[0].startswith('R'):
                    fmt_tag = '<td style="color:white;background-color:' + colors[3] + '">' + tags_dict[tag_info[0]] + '</td>'
                else:
                    fmt_tag = '<td>' + tags_dict[tag_info[0]] + '</td>'
                output_string += '<tr> <td>' + tag_info[0] + fmt_tag + '<td>' + str(tag_info[1])
            else:
                output_string += '<tr> <td>' + tag_info[0] + '<td> <td>' + str(tag_info[1])

    output_string +=  "</table>"
    cnt += 1
    return output_string, file_string, txt_hl

#write results to file, save file, allow for download, delete file

def result(request):
    if request.user.is_authenticated:
        base = "base.html"
    else:
        base = "guest_base.html"

    if request.method == 'POST':
        algorithm = request.POST.get("algorithm")
        input_text = request.POST.get("textInput")
        if len(request.FILES) == 0 and input_text == '':
            context = {
                'output_error_text': "<br>You didn't enter any text or files!<br><br>"
            }
            return render(request, 'result.html', context = context)
        if len(request.FILES) != 0:
            file = request.FILES['fileInput']
            user = request.user
            txt = file.read()
            txt=str(txt,'utf-8')
        if input_text != '':
            txt = input_text
        sw = request.POST.get("sws")
        num_of_topics = request.POST.get("ldarange")
        filename = 'output-' + str(date.today()) + '.txt'
        filepath = "/" + "(^output-.*$)"
        fileList = glob.glob(filepath)
        for filePath in fileList:
            try:
                os.remove(filePath)
            except OSError:
                print("Error while deleting file")
        if algorithm == 'tfidf':
            try:
                textout, newtext = tfidfprocess(txt, txt, sw)
            except ValueError:
                context = {
                    'output_error_text': "<br><br>The text you input likely contains only stopwords. Try again.",
                }
                return render(request, 'result.html', context=context)
            context = {
                'base': base,
                'text': textout,
                'newtext': newtext,
                'algorithm': 'tfidf'
            }
            return render(request, 'result.html', context = context)
        if algorithm == 'pos':
            outputstring, file_string, textout = posprocess(txt, txt, sw)
            #change outputstring to formatted with txt file
            file1 = open(filename,"w+")
            file1.write(file_string)
            file1.close()
            freq_display_str = outputstring.replace("\n", "<br>")
            context = {
               'base': base,
               'text': textout,
               'outputstring': outputstring,
               'algorithm': 'pos',
               'freq_display_str': freq_display_str,
            }
            return render(request, 'result.html', context= context)
        if algorithm == 'lda':
            try:
                outputstring, file_string, textout = ldaprocess(txt, txt, sw, num_of_topics)
            except ValueError:
                context = {
                    'output_error_text': "<br><br>The text you input does not contain enough unique terms for LDA!",
                }
                return render(request, 'result.html', context=context)
#change outputstring to formatted with txt file, also add for frequencies
            file1 = open(filename,"w+")
            file1.write(file_string)
            file1.close()
            context = {
                'base': base,
                'text': textout,
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
    fl_path = 'output-' + str(date.today()) + '.txt'
    filename = 'output-' + str(date.today()) + '.txt'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename="%s"' %filename
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
            return redirect("/recentlyused")
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
            return redirect("/recentlyused")
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
    filename = 'output-' + str(date.today()) + '.txt'
    filepath = "/" + "(^output-.*$)"
    fileList = glob.glob(filepath)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")
    txt = doc.text
    check_txt = txt.replace(' ', '')
    if check_txt == '':
        context = {
            'output_error_text': "<br>The document is empty!<br><br>"
        }
        return render(request, 'result.html', context = context)
    sw = request.POST.get('sws')
    try:
        textout, newtext = tfidfprocess(txt, txt, sw)
    except ValueError:
        context = {
            'output_error_text': "<br><br>The text you input likely contains only stopwords. Try again.",
        }
        return render(request, 'result.html', context=context)
    context = {
        'text': textout,
        'newtext': newtext,
        'algorithm': 'tfidf'
    }
    return render(request, 'result.html', context = context)

def analyze_doc_pos(request, document_id):
    Document = apps.get_model('accounts', 'Document')
    doc = Document.objects.get(pk=document_id)
    filename = 'output-' + str(date.today()) + '.txt'
    filepath = "/" + "(^output-.*$)"
    fileList = glob.glob(filepath)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")
    txt = doc.text
    check_txt = txt.replace(' ', '')
    if check_txt == '':
        context = {
            'output_error_text': "<br>The document is empty!<br><br>"
        }
        return render(request, 'result.html', context = context)
    sw = request.POST.get('sws')
    outputstring, file_string, textout = posprocess(txt, txt, sw)
#change outputstring to formatted with txt file
    file1 = open(filename,"w+")
    file1.write(file_string)
    file1.close()
    freq_display_str = outputstring.replace("\n", "<br>")
    context = {
        'text': textout,
        'outputstring': outputstring,
        'algorithm': 'pos',
        'freq_display_str': freq_display_str,
    }
    return render(request, 'result.html', context= context)

def analyze_doc_lda(request, document_id):
    Document = apps.get_model('accounts', 'Document')
    doc = Document.objects.get(pk=document_id)
    filename = 'output-' + str(date.today()) + '.txt'
    num_of_topics = request.POST.get("numoftopics")
    filepath = "/" + "(^output-.*$)"
    fileList = glob.glob(filepath)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")
    txt = doc.text
    check_txt = txt.replace(' ', '')
    if check_txt == '':
        context = {
            'output_error_text': "<br>The document is empty!<br><br>"
        }
        return render(request, 'result.html', context = context)
    sw = request.POST.get('sws')
    try:
        outputstring, file_string, textout = ldaprocess(txt, txt, sw, num_of_topics)
    except ValueError:
        context = {
            'output_error_text': "<br><br>The text you input does not contain enough unique terms for LDA!",
        }
        return render(request, 'result.html', context=context)
#change outputstring to formatted with txt file, also add for frequencies
    file1 = open(filename,"w+")
    file1.write(file_string)
    file1.close()
    outputstring = outputstring.replace("\n", "<br>")
    context = {
        'text': textout,
        'outputstring': outputstring,
        'algorithm': 'lda'
    }
    return render(request, 'result.html', context=context)


#change to redirect
def delete_project(request, project_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    docs = Document.objects.filter(project = project_id)
    project = Project.objects.get(pk = project_id)
    docs.delete()
    project.delete()
    user = request.user
    project_list=Project.objects.filter(owner=user.id)
    context = {
        'proj_list': project_list,
    }
    return redirect("recentlyused")

#change to redirect
def edit_project_title(request, project_id):
    if request.method == 'POST':
        new_name = request.POST.get("newtitleinput")
        Project = apps.get_model('accounts', 'Project')
        Document = apps.get_model('accounts', 'Document')
        Project.objects.filter(pk=project_id).update(title=new_name)
        documents = Document.objects.filter(project=project_id)
        proj = Project.objects.get(pk=project_id)
        title = proj.title
        context= {
            'doc_list': documents,
            'project': proj,
            'title': title,
        }
        return redirect("project_detail", project_id = proj.id)

#change to redirect
def delete_document(request, document_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    doc = Document.objects.get(pk=document_id)
    proj = doc.project
    proj_id = proj.id
    doc.delete()
    docs_after = Document.objects.filter(project=proj_id)
    if len(docs_after) > 0:
        title = proj.title
        context= {
            'doc_list': docs_after,
            'project': proj,
            'title': title,
        }
        return redirect("project_detail", project_id = proj_id)
    else:
        proj.delete()
        user = request.user
        project_list=Project.objects.filter(owner=user.id)
        context = {
            'proj_list': project_list,
        }
        return redirect("recentlyused")

def edit_document(request, document_id):
    if request.method == 'POST':
        new_text = request.POST.get("editdocinput")
        Project = apps.get_model('accounts', 'Project')
        Document = apps.get_model('accounts', 'Document')
        Document.objects.filter(pk=document_id).update(text=new_text)
        doc = Document.objects.get(pk=document_id)
        proj = doc.project
        proj_id = proj.id
        return redirect("project_detail", project_id = proj.id)

def multi_tfidf(request, project_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    proj = Project.objects.get(pk=project_id)
    docs = Document.objects.filter(project=proj)
    entire_text = ""
    present_text = ""
    i = 0
    for doc in docs:
        i = i + 1
        text = doc.text
        present_text = present_text + "<strong>Document " + str(i) + "</strong>\r\n" + text + "\r\n"
        #text = text.replace("\r\n", "")
        entire_text = entire_text + text + "\r\n"
    check_txt = entire_text.replace(' ', '')
    if check_txt == '':
        context = {
            'output_error_text': "<br>The document is empty!<br><br>"
        }
        return render(request, 'result.html', context = context)
    sw = request.POST.get('sws')
    try:
        textout, newtext = tfidfprocess(entire_text, present_text, sw)
    except ValueError:
        context = {
            'output_error_text': "<br><br>The text you input likely contains only stopwords. Try again.",
        }
        return render(request, 'result.html', context=context)
    '''
    filename = 'output-' + str(date.today()) + '.txt'
    try:
        os.remove(filename)
    except:
        print('file not found exception')
    '''
    #txt = clean_up(present_text)
    #present_text = '<br><br>'.join(txt)
    context = {
        'text': textout,
        'newtext': newtext,
        'algorithm': 'tfidf'
    }
    return render(request, 'result.html', context = context)

def multi_pos(request, project_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    filename = 'output-' + str(date.today()) + '.txt'
    filepath = "/" + "(^output-.*$)"
    fileList = glob.glob(filepath)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")
    proj = Project.objects.get(pk=project_id)
    docs = Document.objects.filter(project=proj)
    entire_text = ""
    present_text = ""
    i = 0
    sw = request.POST.get('sws')
    for doc in docs:
        i = i + 1
        text = doc.text
        present_text += "<br><br><strong>Document " + str(i) + "</strong><br> "
        present_text += text
        #text = text.replace("\r\n", "")
        entire_text = entire_text + text + "\r\n"
    check_txt = entire_text.replace(' ', '')
    if check_txt == '':
        context = {
            'output_error_text': "<br>The document is empty!<br><br>"
        }
        return render(request, 'result.html', context = context)
    outputstring, file_string, textout = posprocess(entire_text, present_text, sw)
#change outputstring to formatted with txt file
    file1 = open(filename,"w+")
    file1.write(file_string)
    file1.close()
    freq_display_str = outputstring.replace("\n", "<br>")
    context = {
        'text': textout,
        'outputstring': outputstring,
        'algorithm': 'pos',
        'freq_display_str': freq_display_str,
    }
    return render(request, 'result.html', context= context)

def multi_lda(request, project_id):
    Project = apps.get_model('accounts', 'Project')
    Document = apps.get_model('accounts', 'Document')
    filename = 'output-' + str(date.today()) + '.txt'
    filepath = "/" + "(^output-.*$)"
    fileList = glob.glob(filepath)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")
    proj = Project.objects.get(pk=project_id)
    docs = Document.objects.filter(project=proj)
    entire_text = ""
    present_text = ""
    i = 0
    for doc in docs:
        i = i + 1
        text = doc.text
        present_text = present_text + "<strong>Document " + str(i) + "</strong>\r\n" + text + "\r\n"
        text = text.replace("\r\n", "")
        entire_text = entire_text + text + "\r\n"
    check_txt = entire_text.replace(' ', '')
    if check_txt == '':
        context = {
            'output_error_text': "<br>The document is empty!<br><br>"
        }
        return render(request, 'result.html', context = context)
    sw = request.POST.get('sws')
    num_of_topics = request.POST.get('numoftopics')
    try:
        outputstring, file_string, textout = ldaprocess(entire_text, present_text, sw, num_of_topics)
    except ValueError:
        context = {
            'output_error_text': "<br><br>The text you input does not contain enough unique terms for LDA!",
        }
        return render(request, 'result.html', context=context)
#change outputstring to formatted with txt file, also add for frequencies
    file1 = open(filename,"w+")
    file1.write(file_string)
    file1.close()
    #txt = clean_up(present_text)
    #textout = '<br><br>'.join(txt)
    outputstring = outputstring.replace("\n", "<br>")
    context = {
        'text': textout,
        'outputstring': outputstring,
        'algorithm': 'lda'
    }
    return render(request, 'result.html', context=context)



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
    stopwords = text.ENGLISH_STOP_WORDS.union(user_stopwords)
    return stopwords

def tfidfprocess(txt, present_txt, sw):
    txt = clean_up(txt)
    present_txt = clean_up(present_txt)
    sws = make_sw_list(sw)
    filename = 'output-' + str(date.today()) + '.txt'
    tfidf(txt, present_txt, sws)[0].to_csv(filename, header=None, index=None, sep=' ', mode='w')
    newtext = tfidf(txt, present_txt, sws)[1]
    #textout = '<br>'.join(txt)
    textout = tfidf(txt, present_txt, sws)[2]
    return textout, newtext

#needs work
def posprocess(txt, present_txt, sw):
    txt = clean_up(txt)
    outputstring, file_string, textout = pos(txt, present_txt, sw)
    return outputstring, file_string, textout

def ldaprocess(txt, present_txt, sw, numberoftopics):
    txt = clean_up(txt)
    present_txt = clean_up(present_txt)
    outputstring, file_string, newtext = lda(txt, present_txt, sw, numberoftopics)
    return outputstring, file_string, newtext

#TODO (Ainsley):
#error message in case all text entered consists of stopwords (single, multi, and input)
#css work on submit/back button on project creation page
