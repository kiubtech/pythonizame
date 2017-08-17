# -*- coding: utf-8 -*-
from django.conf.urls import url
from pythonizame.apps.books.views import BooksMainView, BookDetailView, PreviewBookDetailView
from .feeds import LatestEntriesFeed

app_name = "books"

urlpatterns = [
    url(r'^books/$', BooksMainView.as_view(), name="index"),
    url(r'^books/page/(?P<page>[0-9]+)/$', BooksMainView.as_view(), name='index_paginated'),
    url(r'^books/rss/$', LatestEntriesFeed()),
    url(r'^book/(?P<slug>[-_\w]+)/$', BookDetailView.as_view(), name='detail'),
    url(r'^book/(?P<slug>[-_\w]+)/preview/$', PreviewBookDetailView.as_view(), name='book_preview'),
]
