from pythonizame.core.aws import MEDIAFILES_LOCATION
from storages.backends.s3boto import S3BotoStorage


class MediaStorage(S3BotoStorage):
    location = MEDIAFILES_LOCATION
