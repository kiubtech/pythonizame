from django.conf.urls import url
from pythonizame.apps.blog.webservices.views import AddPostLike, AddPostFavorite

app_name = "ws"

urlpatterns = [
    url(r'add/like/$', AddPostLike.as_view(), name='add_like'),
    url(r'add/favorite/$', AddPostFavorite.as_view(), name='add_favorite'),
]
