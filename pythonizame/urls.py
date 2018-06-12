from django.conf.urls import include, url
from django.contrib.flatpages import views
from django.contrib import admin
from django.conf.urls.static import static
from pythonizame.core.json_settings import json_settings

settings = json_settings()

urlpatterns = [
    url(r'^pymin/', include(admin.site.urls)),
    url(r'^videos/', include('pythonizame.apps.videos.urls', namespace='videos')),
    url(r'^', include('pythonizame.apps.books.urls', namespace='books')),
    url(r'^', include('pythonizame.apps.blog.urls', namespace='blog')),
    url(r'^account/', include('pythonizame.apps.account.urls', namespace='account')),
    url(r'^security/', include('pythonizame.apps.security.urls', namespace='security')),
    url(r'^jobboard/', include('pythonizame.apps.jobboard.urls', namespace='jobboard')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if not settings['AMAZON']['S3']['USE_S3']:
    from pythonizame import settings as setts
    urlpatterns += static(setts.MEDIA_URL, document_root=setts.MEDIA_ROOT)


urlpatterns += [
    url(r'^(?P<url>.*/)$', views.flatpage),
]
