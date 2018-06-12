from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from slugify import slugify
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.core.cache import cache
from django.views.generic import View, DetailView
from .models import PlayList, Video, VideoCategory
from .functions import video_search


class IndexView(View):
    template_name = "video_list.html"

    def get(self, request):
        """
        Devolvemos consulta de publicaciones al usuario
        """
        if 'q' in request.GET and request.GET['q']:
            search_words = request.GET['q']
            queryset = video_search(search_words)
        else:
            search_words = ""
            queryset = PlayList.objects.filter(status=1).order_by('-timestamp')
        paginator = Paginator(queryset, 18)  # 18 elementos
        if 'page' in request.GET and request.GET['page']:
            my_page = int(request.GET['page'])
        else:
            my_page = 1
        try:
            object_list = paginator.page(my_page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        categories = VideoCategory.objects.all()
        ctx = {'object_list': object_list,
               'categories': categories,
               'page_obj': object_list,
               'queryset': search_words}
        return render(request, self.template_name, ctx)


class PlayListVideosView(DetailView):
    template_name = "playlist_detail.html"
    model = PlayList

    def get_object(self, queryset=None):
        obj = super(PlayListVideosView, self).get_object(queryset)
        if obj.status == 1:  # Solo se muestra si está autorizada la visualización
            return obj
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(PlayListVideosView, self).get_context_data(**kwargs)
        actual_playlist = context['playlist']  # Post consultado
        # Obtenemos los post relacionados
        cache_categories = cache.get('pythonizame_videos_categories')
        if cache_categories:
            queryset = cache_categories
        else:
            queryset = VideoCategory.objects.all()
            cache.set('pythonizame_video_categories', queryset, 60 * 5)  # Cache por 15 mins
        context['categories'] = queryset
        related_posts = PlayList.objects.filter(status=1,
                                                categories__in=actual_playlist.categories.all()
                                                ).exclude(id=actual_playlist.id).distinct().order_by('?')[:5]
        context['related_posts'] = related_posts
        return context
