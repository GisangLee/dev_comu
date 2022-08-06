from .common import *

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("MYSQL_ENGINE"),
        "NAME": os.environ.get("MYSQL_NAME"),
        "USER":os.environ.get("MYSQL_USERNAME"),
        "PASSWORD":os.environ.get("MYSQL_PASSWORD"),
        "HOST":os.environ.get("MYSQL_HOST"),
        "PORT":os.environ.get("MYSQL_PORT"),
        #"OPTIONS": {
            #"charset": "utfmb4",
            #"use_unicode": True 
        #}
    }
}


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJ_APPS

STATIC_ROOT = os.path.join(PROJ_DIR, "static")