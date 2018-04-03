from pythonizame.core.json_settings import json_settings

settings = json_settings()

# ==============================================
# CONFIGURACIÓN PARA DJANGO-STORAGE CON BOTO
# ==============================================

AWS_ACCESS_KEY_ID = settings['AMAZON']['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = settings['AMAZON']['AWS_SECRET_ACCESS_KEY']

# ================================================
# CONFIGURACIÓN PARA DJANGO-STORAGE S3 CON BOTO
# ================================================

AWS_STORAGE_BUCKET_NAME = settings['AMAZON']['S3']['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = settings['AMAZON']['S3']['AWS_S3_CUSTOM_DOMAIN']
MEDIAFILES_LOCATION = settings['AMAZON']['S3']['MEDIAFILES_LOCATION']

