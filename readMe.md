# Text Penguin

This program is an SPA where the user can upload a document that is a .pdf or .docx in order to have the contents of the document analyzed by three different algorithms:
Term Frequency-Inverse Document Frequency, Sentiment Analysis, and Latent Direchlet Allocation. The documents can be saved in files called "Projects", which will act as a means to organize the documents for a single project if need be.
The projects can be accessed later by the user as long as they have created a login.

# Technologies

In order to build this project, you will need to install:

* [Python3](https://www.python.org/downloads/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [Django](https://docs.djangoproject.com/en/2.2/topics/install/)

After downloading Python3 and Pip from the websites shown above, you can install Django (on Ubuntu) using:
```
pip install Django
```

# Running

To run the app on your laptop, log into the virtual environment and use the Linux command:
```
source env/bin/activate
python3 manage.py runserver
```


## Deployment
Deployment utilized [Heroku's](https://www.heroku.com/home) deployment platform.  The deployment can be found here: [Text Penguin](http://textpenguin.herokuapp.com/)

Notes about deployment:
*download output file currently not functional in deployment, but works in local development environment.
*must be logged in to create a project, otherwise error occurs
*upload file function not currently in production
*text must be entered with a new line separating each "document"

## Testing

## Authors

|Name:                 |Gmail:                                |
|----------------------|--------------------------------------|
|Samyu Comandur        |samyuktha.comandur@gmail.com          |
|Ainsley McWaters      |mcwatera@gmail.com                    |
|Suzie Prentice        |suzanneprentice26@gmail.com           |
|Matt O’Neill          |matthew.oneill71@gmail.com            |
|Steven Maxwell        |maxwellstevene@gmail.com              |
