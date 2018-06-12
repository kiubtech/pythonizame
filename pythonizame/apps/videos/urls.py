from django.conf.urls import url, include
from pythonizame.apps.videos.views import IndexView, PlayListVideosView

app_name = "videos"


urlpatterns = [
    url(r'^$', (IndexView.as_view()), name="list"),
    url(r'^(?P<slug>[-_\w]+)/$', (PlayListVideosView.as_view()), name='playlist-detail'),
    # url(r'^blog/rss/$', LatestEntriesFeed()),
    # url(r'^post/new/$', (PostNew.as_view()), name='new_post'),
    # url(r'^author/([-_\w]+)/$', (ByAuthorView.as_view()), name='by_author'),
    # url(r'^author/([-_\w]+)/page/([0-9]+)/$', ByAuthorView.as_view(), name='by_author_paginated'),
    # url(r'^category/([-_\w]+)/$', ByCategoryView.as_view(), name='by_category'),
    # url(r'^category/([-_\w]+)/page/([0-9]+)/$', ByCategoryView.as_view(),
    #     name='by_category_paginated'),
    # url(r'^tag/([-_\w]+)/$', ByTagView.as_view(), name='by_tag'),
    # url(r'^tag/([-_\w]+)/page/([0-9]+)/$', ByTagView.as_view(), name='by_tag_paginated'),
    # url(r'^(?P<slug>[-_\w]+)/preview/$', PreviewPostDetailView.as_view(), name='post_preview'),
]
