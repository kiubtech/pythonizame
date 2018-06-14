from pythonizame.core.json_settings import json_settings

settings = json_settings()

BEFORE_DJANGO_APPS = (

)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
)

LOCAL_APPS = (
    'pythonizame.apps.website',
    'pythonizame.apps.blog',
    'pythonizame.apps.account',
    'pythonizame.apps.security',
    'pythonizame.apps.books',
    'pythonizame.apps.jobboard',
    'pythonizame.apps.videos'
)

THIRD_PARTY_APPS = (
    'easy_thumbnails',
    'ckeditor',
    'solo',
    'django_countries',
    'widget_tweaks',
    'storages',
)

if not settings['DEBUG']:  # Solo aplica si se encuentra en servidor de producción.
    THIRD_PARTY_APPS += ('redisboard', )


INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
