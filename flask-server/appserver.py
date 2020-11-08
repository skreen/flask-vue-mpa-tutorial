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