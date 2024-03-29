"""Main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('accounts/', include('accounts.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('', views.home, name='home'),
    path('result/', views.result, name='result'),
	path('recentlyused/', views.recentlyused, name='recentlyused'),
	path('resources/', TemplateView.as_view(template_name='resources.html'), name='resources'),
    path('guestresources/', TemplateView.as_view(template_name='guestresources.html'), name='guestresources'),
    path('guestabout/', TemplateView.as_view(template_name='guestabout.html'), name='guestabout'),
	path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('guesthome/', TemplateView.as_view(template_name='guesthome.html'), name='guesthome'),
    path('Content-Disposition/', views.download_file), 
    path('createProject/',  views.createProject, name='createProject'),
    path('recentlyused/<int:project_id>/', views.project_detail, name='project_detail'),
    path('deleteallobjects/', views.delete_all_projects, name="delete_all_projects"),
    path('addDocument/<int:project_id>/', views.add_document, name="add_document"),
    path('analyzeDocTFIDF/<int:document_id>', views.analyze_doc_tfidf, name="analyze_doc_tfidf"),
    path('analyzeDocLDA/<int:document_id>', views.analyze_doc_lda, name="analyze_doc_lda"),
    path('analyzeDocPOS/<int:document_id>', views.analyze_doc_pos, name="analyze_doc_pos"),
    path('deleteProject/<int:project_id>/', views.delete_project, name='delete_project'),
    path('editProjectTitle/<int:project_id>/', views.edit_project_title, name="edit_project_title"),
    path('deleteDocument/<int:document_id>/', views.delete_document, name="delete_document"),
    path('editDocument/<int:document_id>/', views.edit_document, name="edit_document"),
    path('tfidfMultiAnalyze/<int:project_id>/', views.multi_tfidf, name="multi_tfidf"),
    path('posMultiAnalyze/<int:project_id>/', views.multi_pos, name="multi_pos"),
    path('ldaMultiAnalyze/<int:project_id>/', views.multi_lda, name="multi_lda"),
]
