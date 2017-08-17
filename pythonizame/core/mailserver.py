from pythonizame.core.json_settings import json_settings

settings = json_settings()


EMAIL_USE_TLS = settings['EMAIL']['EMAIL_USE_TLS']
EMAIL_HOST = settings['EMAIL']['EMAIL_HOST']
EMAIL_PORT = settings['EMAIL']['EMAIL_PORT']
EMAIL_HOST_USER = settings['EMAIL']['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = settings['EMAIL']['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = settings['EMAIL']['DEFAULT_FROM_EMAIL']
