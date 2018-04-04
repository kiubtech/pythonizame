import os
import uuid
from django.db import models
from django.contrib.flatpages.models import FlatPage as FlatPageOld
from solo.models import SingletonModel


def website_logo(self, filename):
    path = "general-settings/"
    ext = filename.split('.')[-1]
    my_filename = "{0}.{1}".format(str(uuid.uuid4()).replace('-', ''), ext)
    url = os.path.join(path, my_filename)
    return url


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Nombre del sitio')
    logo = models.ImageField(upload_to=website_logo, null=True, blank=True)
    favicon = models.ImageField(upload_to=website_logo, null=True, blank=True)
    enable_disqus = models.BooleanField(default=False)
    disqus_shortname = models.CharField(max_length=1000, null=True, blank=True,
                                        help_text="Shortname proporcionado por disqus")
    facebook = models.URLField(max_length=1000, null=True, blank=True)
    instagram = models.URLField(max_length=1000, null=True, blank=True)
    pinterest = models.URLField(max_length=1000, null=True, blank=True)
    twitter = models.URLField(max_length=1000, null=True, blank=True)
    gplus = models.URLField(max_length=1000, null=True, blank=True, help_text="Google Plus")
    google_analytics = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class FlatPage(FlatPageOld):

    STATUS_CHOICES = (
        (0, "Oculto"),
        (1, "Visible")
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, help_text="¿Define si es oculto o visible?")
