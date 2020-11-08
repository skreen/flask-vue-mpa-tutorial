# flask-vue-mpa-tutorial
A setup guide for flask + MPA vue that does not used index template from vue

## Requirements

This is written for use on Windows 10 with powershell.

You should also have [python3](https://www.python.org) installed and venv, which should come with python3.

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
+.venv
+flask-server
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







