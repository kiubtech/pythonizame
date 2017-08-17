from __future__ import unicode_literals

import os
import uuid
import logging

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.cache import cache

from ckeditor_uploader.fields import RichTextUploadingField
from easy_thumbnails.files import get_thumbnailer

from pythonizame.apps.global_functions import get_cleaned_uuid

# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


def image_path_post(self, filename):
    today = timezone.now()
    path = "Post/{0}/{1}/{2}/".format(today.year, today.month, today.day)
    ext = filename.split('.')[-1]
    my_filename = "{0}.{1}".format(str(uuid.uuid1()).replace('-', ''), ext)
    url = os.path.join(path, my_filename)
    return url


class Category(models.Model):
    name = models.CharField(max_length=400, unique=True)
    slug = models.SlugField(max_length=600, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría de Blog"
        verbose_name_plural = "Categorías de Blog"

    @property
    def num_published_post(self):
        """
        Retorna el numero de post publicados de la categoría
        """
        try:
            _num = Post.objects.filter(published=True).count()
        except:
            _num = 0
        return _num


class TagPost(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag de Post"
        verbose_name_plural = "Tags de Post"


class Post(models.Model):
    author = models.ForeignKey(User, help_text='Autor', related_name='autor')
    pin_image = models.ImageField(max_length=1000, upload_to=image_path_post)
    main_image = models.ImageField(max_length=1000, upload_to=image_path_post)
    author_image = models.CharField(max_length=500, null=True, blank=True,
                                    help_text="Llenar si la imagen requiere referencia de su autor")
    author_link = models.URLField(max_length=10000, null=True, blank=True,
                                  help_text="URL de referencia al autor.")
    title = models.CharField(max_length=800)
    slug = models.SlugField(max_length=600, unique=True)
    abstract = models.TextField(max_length=200, help_text='Máximo 200 caracteres. Texto principal de la presentación')
    content = RichTextUploadingField(max_length=1000000)
    tags = models.ManyToManyField(TagPost, blank=True)
    categories = models.ManyToManyField(Category)
    published = models.BooleanField(default=False, help_text="Activar para hacer visible en la web")
    publication_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"

    @property
    def pin_image_thumbnail(self):
        if self.pin_image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("post", "pin_image", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.pin_image)['pin_blog_image'].url
                    cache.set(cache_key, thumb_url, 60 * 3)
                    return thumb_url
            except:
                return self.pin_image.url
        else:
            return ""

    @property
    def main_image_thumbnail(self):
        if self.main_image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("post", "main_image", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.main_image)['main_blog_image'].url
                    cache.set(cache_key, thumb_url, 60 * 3)
                    return thumb_url
            except:
                return self.pin_image.url
        else:
            return ""

    @property
    def related_post_image_thumbnail(self):
        if self.pin_image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("post", "pin_image", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.pin_image)['pin_blog_image'].url
                    cache.set(cache_key, thumb_url, 60 * 3)
                    return thumb_url
            except:
                return self.pin_image.url
        else:
            return ""

    @property
    def url(self):
        return "http://pythoniza.me/{0}".format(self.slug)

    @property
    def num_likes(self):
        try:
            likes = LikePost.objects.filter(post__id=self.id).count()
        except:
            likes = 0
        return likes

    def i_like(self, user_id):
        try:
            LikePost.objects.get(post=self, created_by=user_id)
            return True
        except:
            return False

    def i_favorite(self, user_id):
        try:
            FavoritePost.objects.get(post=self, created_by=user_id)
            return True
        except:
            return False

    def preview(self):
        url = "<a href='/%s/preview/' target='_blank'>Vista Previa</a>" % self.slug
        return url

    preview.allow_tags = True


class LikePost(models.Model):
    id = models.UUIDField(primary_key=True, default=get_cleaned_uuid, editable=False)
    created_by = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        unique_together = ('created_by', 'post')
        verbose_name = "Like de Post"
        verbose_name_plural = "Likes de Post"


class FavoritePost(models.Model):
    id = models.UUIDField(primary_key=True, default=get_cleaned_uuid, editable=False)
    created_by = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        unique_together = ('created_by', 'post')
        verbose_name = "Post Favorito"
        verbose_name_plural = "Post Favorito"
