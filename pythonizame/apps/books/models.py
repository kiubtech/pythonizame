# -*- coding: utf-8 -*-
import sys
import logging
import os
import uuid
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.cache import cache

from easy_thumbnails.files import get_thumbnailer
from ckeditor_uploader.fields import RichTextUploadingField

from pythonizame.apps.global_functions import format_sys_errors


logger = logging.getLogger(__name__)


def image_path_book(self, filename):
    path = "Book/{0}/image/".format(str(self.slug))
    ext = filename.split('.')[-1]
    my_filename = "{0}.{1}".format(str(uuid.uuid1()), ext)
    url = os.path.join(path, my_filename)
    return url


def file_path_book(self, filename):
    path = "Book/{0}/file/".format(str(self.slug))
    ext = filename.split('.')[-1]
    my_filename = "{0}.{1}".format(str(uuid.uuid1()), ext)
    url = os.path.join(path, my_filename)
    return url


@python_2_unicode_compatible
class BookCategory(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=600)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría de Libro"
        verbose_name_plural = "Categorías de Libros"


@python_2_unicode_compatible
class TagBook(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag de Libro"
        verbose_name_plural = "Tags de Libros"


@python_2_unicode_compatible
class Book(models.Model):
    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=800)
    slug = models.SlugField(max_length=1000, unique=True)
    image = models.ImageField(max_length=1000, upload_to=image_path_book, null=True, blank=True,
                              help_text="Imagen de Portada")
    file = models.FileField(max_length=1000, upload_to=file_path_book, null=True, blank=True)
    description = RichTextUploadingField(max_length=20000)
    author = models.CharField(max_length=500, help_text="Autor del libro")
    url = models.URLField(max_length=800, help_text="Url de la fuente donde se consulta la información")
    categories = models.ManyToManyField(BookCategory)
    tags = models.ManyToManyField(TagBook, blank=True)
    published = models.BooleanField(default=False)
    publication_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    @property
    def related_book_image_thumbnail(self):
        if self.image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("book", "pin_image", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.pin_image)['pin_book_image'].url
                    cache.set(cache_key, thumb_url, 60 * 3)
                    return thumb_url
            except:
                return self.image.url
        else:
            return ""


    @property
    def image_thumbnail(self):
        if self.image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("book", "image", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.image)['book_image'].url
                    cache.set(cache_key, thumb_url, 60*60)
                    return thumb_url
            except:
                logger.error(format_sys_errors(sys, with_traceback=True))
                return self.image.url
        else:
            return "https://www.awm.gov.au/sites/default/files/book-cover-british-official-red-cover.jpg"

    def preview(self):
        url = "<a href='/book/%s/preview/' target='_blank'>Vista Previa</a>" % self.slug
        return url
    preview.allow_tags = True
