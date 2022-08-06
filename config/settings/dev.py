from .common import *

DEBUG = True

ALLOWED_HOSTS = []

THIRD_PARTY_APPS += [
    "debug_toolbar"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJ_APPS

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

print(f"THIRD_PARTY_APPS : {THIRD_PARTY_APPS}")
print(f"MIDDLEWARE : {MIDDLEWARE}")
print(f"INSTALLED_APPS : {INSTALLED_APPS}")

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("MYSQL_ENGINE"),
        "NAME": os.environ.get("MYSQL_NAME"),
        "USER":os.environ.get("MYSQL_USERNAME"),
        "PASSWORD":os.environ.get("MYSQL_PASSWORD"),
        "HOST":os.environ.get("MYSQL_HOST"),
        "PORT":os.environ.get("MYSQL_PORT"),
        #"OPTIONS": {
            #"charset": 'utfmb4',
            #"use_unicode": True 
        #}
    }
}

STATICFILES_DIRS = [
     os.path.join(PROJ_DIR, "static")
]

#STATIC_ROOT = os.path.join(PROJ_DIR, "static")

import socket  # only if you haven't already imported this
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]