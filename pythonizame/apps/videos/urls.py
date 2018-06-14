from django.conf.urls import url, include
from pythonizame.apps.videos.views import IndexView, PlayListVideosView, VideoDetailView

app_name = "videos"


urlpatterns = [
    url(r'^$', (IndexView.as_view()), name="list"),
    url(r'^(?P<slug>[-_\w]+)/$', (PlayListVideosView.as_view()), name='playlist-detail'),
    url(r'^video-detail/(?P<pk>[-_\w]+)/$', (VideoDetailView.as_view()), name='video-detail'),
]
