# flask-vue-mpa-tutorial
A setup guide for flask + MPA vue that does not used index template from vue

## Requirements

This is written for use on Windows 10 with powershell.

You should also have [python3](https://www.python.org) installed and venv, which should come with python3.

npm (node.js) is also required.

## Step 1 - The virtual environment

Create a virtual environment folder, I do this in the root of the cloned github project.

```powershell
py -3 -m venv .venv
```

The virtual environment is responsible for keeping the installation requirments for the flask-app.

You need to activate the virtual environment before anything else. Run the following command

```powershell
.\.venv\Scripts\activate
```

Windows powershell will show a prefix in the command line when you have an active virtual environment. for example like this:

```powershell
(.venv) D:\flask-vue-mpa-tutorial >
```

To deactivate a virtual environment simply run 
```powershell
deactivate
```

When installing packages and running flask it is very important that the virtual environment is active so everthing is installed in your virtual environment.

## Step 2 - install flask

```powershell
pip install flask
```

make a sever folder
```powershell
mkdir flask-server
```

In this folder we add files for flask
create the file

    app.py


The folder structure

```
+ .venv/
+ flask-server
   + app.py
```

And in app.py add the following

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Home page'
```

Now you can run flask

```powershell
(.venv) flask-server> flask run
```

Normally if you had another name of the script it would not start. change name to try it out

kill flask with `ctrl+c` and rename `app.py` to `app2.py` and start flask again to see the error.

If you have any other name than `app.py`
you have to define the name in powershells environmentvariables.

Rename `app.py` to `appserver.py` and set the environment.

```powershell
 (.venv) flask-server > $env:FLASK_APP='appserver.py'
```
Any changes you do to the code while flask is running won't be visible unless you restart flask. This can be done automatically by enabling development mode 

```powershell
(.venv) flask-server > env:FLASK_ENV='development'
```

Right now we can see that setting environment variables everytime we boot up to work isn't ideal. We could ofcourse make a script that sets them for us. But this is the time to introduce dotenv.

## Step 3 - install dotenv

url: https://pypi.org/project/python-dotenv/

Dotenv will help us setup environment variables and is also usefull for setting upp private keys for api since you can add the .env file to the ignore list of github.
There is also and .flaskenv file were you store flask-specific stuff.

```powershell
(.venv) ... > pip install -U python-dotenv
```

### Step 3.1 - flaskenv

create `.flaskenv` file in flask-server directory and add the following

```
FLASK_ENV=development
FLASK_APP=appserver.py
```

now when you run flask from that directory these line will be read.

### Step 3.2 - env

create `.env` in the flask-server directory 
and add

```
SECRET_KEY='This shouldn't be pushed to github'
```

create the file `config.py` and add the following:

```python
"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'

class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get("SECRET_KEY")

class DevConfig(Config):
    DEVELOPMENT = True
    SECRET_KEY = environ.get("SECRET_KEY")
```

This file will be used to store configurations used for production server and development. The correct config will be loaded in `appserver.py` by reading the settings in`.flaskenv`.

Replace `appserver.py` content with the following:

```python
from flask import Flask
from os import environ, path
from dotenv import load_dotenv

app = Flask(__name__)

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.flaskenv'))

if environ.get('FLASK_ENV') == 'development':
    app.config.from_object('config.DevConfig')
else:
    app.config.from_object('config.ProdConfig')

@app.route('/')
def home():
    return 'The very secret key' + app.config['SECRET_KEY'] 
```

If you remove the line with FLASK_ENV or change it to any other value than development in the file .flaskenv the ProdConfig will be used.

current directory structure
```
+ .venv/
+ flaskserver/
|  + .env
|  + .flaskenv
|  + appserver.py
|  + config.py
```

## Step 4 - Jinja and flask directory structure

We will set up a basic structure for flask directories. Create the folders

1. flaskserver/templates

    Used for templates

2. flaskserver/templates/includes

   Used for partial includes into templates

3. flaskserver/static

   Used for static files

4. flaskserver/static/css

    For stylesheets. we will add tailwind later

The directory structure should now contain:
```
+ .venv/
+ flaskserver/
    + static/
    |    + css/
    + templates/
    |    + includes/
|  + .env
|  + .flaskenv
|  + appserver.py
|  + config.py
```

### Step 4.1

Make a simple Jinja template.
Create the new file flask-server/templates/layout.html
and add the following
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask app</title>
</head>
<body>
{% block content%}{% endblock %}
</body>
</html>
```
Create flask-server/templates/home.html
And add 
```html
{% extends 'layout.html' %}
{% block content %}
<h1>Welcome home!</h1>
{% endblock %}
```

Now we need to import `render_template` and use it in `appserver.py`.
This is the final results

```python
from flask import Flask, render_template
from os import environ, path
from dotenv import load_dotenv

app = Flask(__name__)

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.flaskenv'))

if environ.get('FLASK_ENV') == 'development':
    app.config.from_object('config.DevConfig')
else:
    app.config.from_object('config.ProdConfig')

@app.route('/')

def home():
    return render_template('home.html')
```

If you run the server and head to http://127.0.0.1:5000 you will be greeted with the new template.

Before we use the `includes` directory we are going to add tailwind css

Step 5 - tailwind css

in the projet root create the folder tailwindcss
```cmd
mkdir tailwind
cd tailwindcss
npm -y init
```

The npm command is to create the `package.json` file.
Now install tailwind css, remember to run the command from the tailwind folder otherwise you cant uninstall automatically

```cmd
npm install tailwindcss
```

Also generate the tailwind config for future use with

```cmd
npx tailwindcss init
```

While we are at it, make a src folder at `tailwind/src`
and create the file `tailwind/src/style.css`

Add the following content to the file.
```css
@tailwind base;

@tailwind components;

@tailwind utilities;
```

We're going to make a build script for convenience so that the css is built in our flask-server.

Open `tailwind/package.json` and change the script section to the following:

```json
  "scripts": {
    "build": "tailwind build src/style.css -o ../flask-server/static/css/style.css"
  },
```

Then run the command (while in the tailwind folder)
```cmd
npm run build
```
You know have a tailwind.css in your static/css folder.

Step 5.1 - Modifying template to use the css

Open layout.html and add the following to test the stylesheet

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask app</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"/>
</head>
<body class="bg-blue-600 text-white p-4">
{% block content%}{% endblock %}
</body>
</html>
```

