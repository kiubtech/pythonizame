# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from pythonizame.apps.website.views import IndexMainView


urlpatterns = patterns('',
                       url(r'^$', IndexMainView.as_view(), name="index"),
                       )
