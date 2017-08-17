import os
import sys
import json
import uuid

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from django.core.cache import cache

from easy_thumbnails.files import get_thumbnailer
from django.contrib.postgres.fields import JSONField
from pythonizame.core.json_settings import json_settings
from pythonizame.apps.global_functions import format_sys_errors

settings = json_settings()


def image_user_profile_path(self, filename):
    extension = os.path.splitext(filename)[1][1:]
    file_name = os.path.splitext(filename)[0]
    url = "Users/%s/profile/%s.%s" % (self.user.username, slugify(str(file_name)), extension)
    return url


class Power(models.Model):

    def image_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "Powers/image/%s.%s" % (slugify(str(file_name)), extension)
        return url

    name = models.CharField(max_length=200, help_text="Superpoder")
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=image_path)
    python_auxiliary = models.BooleanField(default=False, help_text="Es una tecnología Auxiliar a Python?")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Poder Python"
        verbose_name_plural = "Poderes Python"


class Achievement(models.Model):

    def image_path(self, filename):
        today = timezone.now()
        path = "Achievement/{0}/{1}/{2}/".format(today.year, today.month, today.day)
        ext = filename.split('.')[-1]
        my_filename = "{0}.{1}".format(str(uuid.uuid1()).replace('-', ''), ext)
        url = os.path.join(path, my_filename)
        return url

    name = models.CharField(max_length=400)
    image = models.ImageField(upload_to=image_path)
    description = models.TextField(max_length=400)
    message_for_user = models.TextField(max_length=400, help_text="Mensaje que aparecerá al usuario")
    num_available = models.IntegerField(help_text="Limitado a una cantidad de personas. Ej. 100 primeros registros")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Logro"
        verbose_name_plural = "Logros"

    @property
    def thumbnail(self):
        if self.image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("achievement", "thumbnail", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.image)['achievement_thumbnail'].url
                    cache.set(cache_key, thumb_url, 60 * 120)
                    return thumb_url
            except:
                return self.image.url
        else:
            return ""

    def previous_image(self):
        return '<div align="center"><a href="%s">' \
               '<img src="%s" width=50px heigth=50px/ style="border-radius: 150px;"></a></div>' % (self.thumbnail,
                                                                                                   self.thumbnail)

    previous_image.allow_tags = True


class UserAchievement(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)
    viewed = models.BooleanField(default=False, help_text="Ya lo vio el usuario?")
    date_received = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.achievement, self.user)

    class Meta:
        unique_together = ('achievement', 'user')
        verbose_name = "Logro de usuario"
        verbose_name_plural = "Logros de usuario"


class UserProfile(models.Model):

    GENDER_CHOICES = (
        (0, 'Hombre'),
        (1, 'Mujer'),
    )

    user = models.OneToOneField(User)
    powers = models.ManyToManyField(Power, help_text="Super poderes del usuario")
    image = models.ImageField(upload_to=image_user_profile_path, null=True, blank=True)
    cover_image = models.ImageField(upload_to=image_user_profile_path, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    data = JSONField(null=True, blank=True, help_text="Información adicional")

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    @property
    def gender(self):
        try:
            return json.loads(self.data)['gender']
        except:
            return ""

    @property
    def about_me(self):
        try:
            return json.loads(self.data)['about_me']
        except:
            print(format_sys_errors(sys, with_traceback=True))
            return ""

    @property
    def website(self):
        try:
            return json.loads(self.data)['website']
        except:
            return ""

    @property
    def facebook(self):
        try:
            return json.loads(self.data)['facebook']
        except:
            return ""

    @property
    def twitter(self):
        try:
            return json.loads(self.data)['twitter']
        except:
            return ""

    @property
    def github(self):
        try:
            return json.loads(self.data)['github']
        except:
            return ""

    @property
    def country_code(self):
        try:
            return json.loads(self.data)['country_code']
        except:
            return ""


    @property
    def avatar(self):
        if self.image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("user", "avatar", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.image)['avatar'].url
                    cache.set(cache_key, thumb_url, 60*120)
                    return thumb_url
            except:
                return self.image.url
        else:
            return ""


    @property
    def cover_thumbnail(self):
        if self.cover_image:
            try:
                cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("user", "cover_image", self.id)
                thumbnail_cache = cache.get(cache_key)
                if thumbnail_cache:
                    return thumbnail_cache
                else:
                    thumb_url = get_thumbnailer(self.cover_image)['user_cover_image'].url
                    cache.set(cache_key, thumb_url, 60*120)
                    return thumb_url
            except:
                return self.cover_image.url
        else:
            return ""
