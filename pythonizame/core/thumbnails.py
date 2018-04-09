from .json_settings import json_settings

settings = json_settings()

THUMBNAIL_ALIASES = {
    '': {
        'pin_blog_image': {'size': (350, 350), 'crop': True},
        'pin_book_image': {'size': (350, 350), 'crop': True},
        'main_blog_image': {'size': (900, 480), 'crop': True},
        'book_image': {'size': (400, 400)},
        'user_cover_image': {'size': (700, 400)},
        'avatar': {'size': (100, 100), 'crop': True},
        'achievement_thumbnail': {'size': (100, 100), 'crop': True},
    },
}

if settings['AMAZON']['S3']['USE_S3']:
    THUMBNAIL_DEFAULT_STORAGE = 'pythonizame.core.custom_storages.MediaStorage'


THUMBNAIL_BASEDIR = "thumbs"
