# Text Penguin

This program is an webapp where the user can upload a document using a text box or a .txt in order to have the contents of the document analyzed by three different algorithms:
Term Frequency-Inverse Document Frequency, Part-of-Speech Tagging, and Latent Direchlet Allocation. The documents can be saved in files called "Projects", which will act as a means to organize the documents for a single project if need be.
The projects can be accessed later by the user as long as they have created a login.

# Technologies

In order to build this project, you will need to install:

* [Python3](https://www.python.org/downloads/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [Django](https://docs.djangoproject.com/en/2.2/topics/install/)

After downloading Python3 and Pip from the websites shown above, you should create a virtual environment, if you do not already have one. 
```
python3 -m venv env 
```

Once you are in the virtual environment, you can install Django (on Ubuntu) using:
```
pip install Django
```
If you are still missing any of the dependencies, you can run
```
pip install requirements.txt
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
* download output file currently not functional in deployment, but works in local development environment.
* user must be logged in to create a project, otherwise error occurs
* upload file function not currently in production
* text must be entered with a new line separating each "document"

Testing login:
username: clubpenguin
password: gamecocks

PLEASE LOG OUT AFTER USAGE.  ONLY ONE PERSON MAY BE LOGGED INTO ACCOUNT AT A TIME.

## Testing

To run unit tests, navigate to the directory with the manage.py file and enter command:

`python3 manage.py test`

Tests will return results automatically, as they've been deesigned with the Django testing capabilities.

------------------------------------------------------------------------------------------------

All behavioral tests are found in the behavioral_tests folder under the main directory.

All behavioral tests are found in behavioral_tests.py

To run these tests you will need to download:
* [Selenium WebDriver](https://selenium.dev/)
* [Chromedriver](https://chromedriver.chromium.org/getting-started)
* [Google Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQiAs67yBRC7ARIsAF49CdXCaIEU_NeWPhVZImm3eyi8GQy1ClK_T5cCN30L4XPLMcAiAnwWdwEaAvIMEALw_wcB&gclsrc=aw.ds)

After your installation is complete, you can run the test using `python3 behavioral_tests.py`


## Authors

|Name:                 |Github:                                                  |Gmail:                                |
|----------------------|---------------------------------------------------------|--------------------------------------|
|Ainsley McWaters      |[@mcwatera](https://github.com/mcwatera)                 |mcwatera@gmail.com                    |
|Suzie Prentice        |[@suzanneprentice](https://github.com/suzanneprentice)   |suzanneprentice26@gmail.com           |
|Matt O’Neill          |[@oneillm71](https://github.com/oneillm71)               |matthew.oneill71@gmail.com            |
|Steven Maxwell        |[@sem15](https://github.com/sem15)                       |maxwellstevene@gmail.com              |
