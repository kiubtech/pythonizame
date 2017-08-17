__author__ = 'alex'
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(levelname)s] [%(asctime)s] [%(name)s:%(module)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'system_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '../log/system.log'),
            'formatter': 'verbose'
        },
        'system_2_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '../log/system.log'),
            'formatter': 'verbose'
        },
        'Pythonizame_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '../log/Pythonizame.log'),
            'formatter': 'verbose'
        },
        'Pythonizame_file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '../log/Pythonizame.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['system_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.account': {
            'handlers': ['system_2_file', 'Pythonizame_file_error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'Pythonizame': {
            'handlers': ['Pythonizame_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}