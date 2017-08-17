import os
from pythonizame.core.json_settings import json_settings

settings = json_settings()

__STATIC_PATH = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(__STATIC_PATH, "../pythonizame/static"),
)

if not settings['DEBUG']:
    STATIC_ROOT = os.path.join(__STATIC_PATH, '../static/')
