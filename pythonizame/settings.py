import os
from pythonizame.core.applist import *
from pythonizame.core.logging import *
from pythonizame.core.cache import *
from pythonizame.core.ckeditor import *
from pythonizame.core.aws import *
from pythonizame.core.mediafiles import *
from pythonizame.core.mailserver import *
from pythonizame.core.thumbnails import *
from pythonizame.core.theming import *
from pythonizame.core.staticfiles import *
from pythonizame.core.json_settings import json_settings

settings = json_settings()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = settings["SECRET_KEY"]
SITE_ID = settings['SITE_ID']
DEBUG = settings['DEBUG']
ALLOWED_HOSTS = settings["SECURITY"]["ALLOWED_HOSTS"]
DATABASES = {'default': settings['DB']}


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'pythonizame.urls'

WSGI_APPLICATION = 'pythonizame.wsgi.application'


LANGUAGE_CODE = 'es-MX'
TIME_ZONE = 'America/Merida'
USE_I18N = True
USE_L10N = True
USE_TZ = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pythonizame/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pythonizame.apps.context_processors.website',
            ],
        },
    },
]

AWS_QUERYSTRING_AUTH = False
