from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default="Title")
    
    def __str__(self):
            return Project.title
    
class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
            return Document.text