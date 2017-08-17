from pythonizame.core.json_settings import json_settings

settings = json_settings()

# pythonizame Cache System.
CACHE_WEB_TIME = 60 * settings['CACHE']['CACHE_WEB_TIME_MINUTES']
CACHE_MOVIL_TIME = 60 * settings['CACHE']['CACHE_MOVIL_TIME_MINUTES']


CACHES = {
    "default": {
        "BACKEND": settings['CACHE']['BACKEND'],
        "LOCATION": settings['CACHE']['LOCATION'],
        "OPTIONS": settings['CACHE']['OPTIONS']
    },
}

