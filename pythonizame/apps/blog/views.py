import sys
import logging

from slugify import slugify

from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic import ListView, View

from pythonizame.apps.mixin import LoginRequiredMixin
from pythonizame.apps.account.functions import CheckAchievements
from pythonizame.apps.global_functions import format_sys_errors
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, TagPost
from .functions import blog_search
from .forms import PostForm

# ==========================
# Blog by Entries
# ==========================

# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


class PostNew(LoginRequiredMixin, View):
    template_name = "post_new.html"
    form = PostForm

    def get(self, request):
        ctx = {'categories': Category.objects.all(),
               'tags': TagPost.objects.all(), 'form': self.form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            try:
                tags = TagPost.objects.filter(id__in=request.POST.getlist('post_tags'))
            except:
                tags = None
            try:
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.slug = slugify(new_post.title)
                new_post.save()
                if tags:
                    for tag in tags:
                        new_post.tags.add(tag)
                new_post.save()
                messages.success(request, "Gracias por generar una excelente publicación para la comunidad!")
            except:
                mensaje = format_sys_errors(sys, with_traceback=True)
                logger.error(mensaje)
                messages.error(request, "Ups! algo salió mal, por favor intenta de nuevo")
        else:
            messages.error(request, "Error en los datos recibidos")
        ctx = {'categories': Category.objects.all(),
               'tags': TagPost.objects.all(), 'form': form}
        return render(request, self.template_name, ctx)


class IndexView(View):
    template_name = "index_blog.html"

    @staticmethod
    def get_recent_post():
        """
        Obtenemos las últimas 5 publicaciones
        :return:
        """
        cache_blog_recent_post = cache.get('pythonizame_blog_recent_post')
        if cache_blog_recent_post:
            queryset = cache_blog_recent_post
        else:
            queryset = Post.objects.filter(published=True).order_by('-publication_date')[:5]
            cache.set('pythonizame_blog_recent_post', queryset, 60 * 5)
        return queryset

    def get(self, request):
        """
        Devolvemos consulta de publicaciones al usuario
        """
        if 'q' in request.GET and request.GET['q']:
            search_words = request.GET['q']
            queryset = blog_search(search_words)
        else:
            search_words = ""
            queryset = Post.objects.filter(published=True).order_by('-publication_date')
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
        # ============================================================
        # Revisamos si tiene medallas pendientes.
        # ============================================================
        if self.request.user.is_authenticated():
            logros = CheckAchievements(self.request.user)
            logros_pendientes = logros.get_all_pending_achievements()
            if logros_pendientes:
                for logro in logros_pendientes:
                    logro.viewed = True
                    logro.date_received = timezone.now().date()
                    logro.save()
        else:
            logros_pendientes = None
        ctx = {'object_list': object_list,
               'pending_achievements': logros_pendientes,
               'recent_post': self.get_recent_post(),
               'page_obj': object_list,
               'queryset': search_words,
               'categories': Category.objects.all()}
        return render(request, self.template_name, ctx)


class PostDetailView(DetailView):
    template_name = "post_detail.html"
    model = Post

    def get_object(self, queryset=None):
        obj = super(PostDetailView, self).get_object(queryset)
        if obj.published:  # Solo se muestra si está publicado
            return obj
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        actual_post = context['post']  # Post consultado
        # Obtenemos los post relacionados
        cache_categories = cache.get('pythonizame_post_categories')
        if cache_categories:
            queryset = cache_categories
        else:
            queryset = Category.objects.all()
            cache.set('pythonizame_post_categories', queryset, 60 * 5)  # Cache por 15 mins
        context['categories'] = queryset
        context['i_like'] = actual_post.i_like(self.request.user)
        context['i_favorite'] = actual_post.i_favorite(self.request.user)
        related_posts = Post.objects.filter(published=True,
                                            categories__in=actual_post.categories.all()
                                            ).exclude(id=actual_post.id).distinct().order_by('?')[:5]
        context['related_posts'] = related_posts
        return context


class PreviewPostDetailView(DetailView):
    """
    Vista previa del usuario author de la publicación
    """
    template_name = "post_detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PreviewPostDetailView, self).get_context_data(**kwargs)
        actual_post = context['post']  # Post consultado
        # Obtenemos los post relacionados
        if self.request.user == actual_post.author or self.request.user.is_superuser:
            cache_categories = cache.get('pythonizame_post_categories')
            if cache_categories:
                context['categories'] = cache_categories
            else:
                context['categories'] = Category.objects.all()
                cache.set('pythonizame_post_categories', 60 * 5)  # Cache por 15 mins
            context['i_like'] = actual_post.i_like(self.request.user)
            context['i_favorite'] = actual_post.i_favorite(self.request.user)
            if actual_post.tags.all():
                related_posts = Post.objects.filter(published=True,
                                                    categories=actual_post.categories.all(),
                                                    ).exclude(id=actual_post.id).distinct().order_by('?')[:5]
            else:
                related_posts = Post.objects.filter(published=True,
                                                    categories=actual_post.categories.all()
                                                    ).exclude(id=actual_post.id).distinct().order_by('?')[:5]
            context['related_posts'] = related_posts
            return context
        else:
            raise Http404()


#
# Blog by Author.
#


class ByAuthorView(ListView):
    template_name = 'by_author_blog.html'
    model = Post
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super(ByAuthorView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        try:
            # Si envían el número de página entonces lo realizamos
            context['author'] = self.author
            paginator = context['paginator']
            page_obj = paginator.page(self.args[1])
            context['page_obj'] = page_obj
            context['object_list'] = page_obj.object_list
        except:
            pass
        context['recent_post'] = Post.objects.filter(published=True, created_by=self.author).order_by('?')[:5]
        return context

    def get_queryset(self):
        try:
            self.author = User.objects.get(username=self.args[0])
        except:
            self.author = None
        if self.author:
            publicaciones = Post.objects.filter(published=True, created_by=self.author).order_by('-timestamp')
            return publicaciones
        else:
            raise Http404()


# ==========================
# Blog by Category
# ==========================


class ByCategoryView(ListView):
    template_name = 'by_category_blog.html'
    model = Post
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super(ByCategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        try:
            # Si envían el número de página entonces lo realizamos
            context['category'] = self.category
            paginator = context['paginator']
            page_obj = paginator.page(self.args[1])
            context['page_obj'] = page_obj
            context['object_list'] = page_obj.object_list
        except:
            pass
        context['recent_post'] = Post.objects.filter(published=True, categories=self.category).order_by('?')[:5]
        return context

    def get_queryset(self):
        try:
            self.category = Category.objects.get(slug=self.args[0])
        except:
            self.category = None
        if self.category:
            publicaciones = Post.objects.filter(published=True, categories=self.category).order_by('-timestamp')
            return publicaciones
        else:
            raise Http404()


# ==========================
# Blog by Tag
# ==========================


class ByTagView(ListView):
    template_name = 'by_tag_blog.html'
    model = Post
    paginate_by = 24
    my_tag = None

    def get_context_data(self, **kwargs):
        context = super(ByTagView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        try:
            # Si envían el número de página entonces lo realizamos
            context['tag'] = self.my_tag
            paginator = context['paginator']
            page_obj = paginator.page(self.args[1])
            context['page_obj'] = page_obj
            context['object_list'] = page_obj.object_list
        except:
            pass
        context['recent_post'] = Post.objects.filter(published=True).order_by('?')[:5]
        return context

    def get_queryset(self):
        self.my_tag = str(self.args[0]).strip()
        try:
            obj_tag = TagPost.objects.get(slug=self.my_tag)
        except:
            obj_tag = None
        if obj_tag:
            publicaciones = Post.objects.filter(tags=obj_tag).order_by('-timestamp')
        else:
            publicaciones = None
        return publicaciones
