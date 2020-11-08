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
    SECRET_KEY =  environ.get("SECRET_KEY")

class DevConfig(Config):
    DEVELOPMENT = True
    SECRET_KEY = environ.get("SECRET_KEY")
