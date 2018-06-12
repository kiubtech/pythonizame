import os
import uuid
import logging

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField

# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


def image_path_video(self, filename):
    today = timezone.now()
    path = "videos/{0}/{1}/{2}/".format(today.year, today.month, today.day)
    ext = filename.split('.')[-1]
    my_filename = "{0}.{1}".format(str(uuid.uuid1()).replace('-', ''), ext)
    url = os.path.join(path, my_filename)
    return url


class VideoCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categoría de videos")
        verbose_name_plural = _("Categorías de videos")


class PlayList(models.Model):

    STATUS_LIST = (
        (0, _("No aprobado")),
        (1, _("Aprobado")),
        (2, _("En revisión"))
    )

    title = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(unique=True)
    abstract = models.TextField(max_length=5000)
    description = RichTextUploadingField(max_length=1000000)
    categories = models.ManyToManyField(VideoCategory, help_text=_("Categorías a la que pertenece"))
    cover = models.ImageField(null=True, blank=True, upload_to=image_path_video)
    created_by = models.ForeignKey(User, related_name='created_by')
    author = models.ForeignKey(User, related_name='author')
    status = models.IntegerField(choices=STATUS_LIST, default=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta: 
        verbose_name = _("Lista de reproducción")
        verbose_name_plural = _("Listas de reproducción")


class Video(models.Model):
    created_by = models.ForeignKey(User)
    playlist = models.ForeignKey(PlayList, help_text=_("Lista de reproducción al que pertenece el video"))
    title = models.CharField(max_length=500)
    description = RichTextUploadingField(max_length=1000000)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

