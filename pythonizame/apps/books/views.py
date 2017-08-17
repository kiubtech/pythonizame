from django.core.cache import cache
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from pythonizame.apps.books.models import Book, BookCategory
from .functions import book_search


class BooksMainView(ListView):
    model = Book
    template_name = 'index_book.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super(BooksMainView, self).get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()
        return context

    def get_queryset(self):
        palabras_busqueda = (self.request.GET.get('q'))
        if palabras_busqueda:
            queryset = book_search(palabras_busqueda)
        else:
            cache_blog = cache.get('pythonizame_books')
            if cache_blog:
                queryset = cache_blog
            else:
                queryset = Book.objects.filter(published=True).order_by('-publication_date')
                cache.get('pythonizame_books', 60 * 5)
        return queryset

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(queryset, page_size, orphans=self.get_paginate_orphans(),
                                       allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            page_number = 1  # Si hay un error entonces enviamos la pagina 1
        try:
            page = paginator.page(page_number)
            tupla = (paginator, page, page.object_list, page.has_other_pages())
            return tupla
        except:
            raise Http404("No se encontró el sitio especificado")


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        actual_book = context['book']  # Libro consultado
        related_books = Book.objects.filter(published=True, categories__in=actual_book.categories.all()
                                            ).exclude(id=actual_book.id).distinct().order_by('?')[:5]
        context['categories'] = BookCategory.objects.all()
        context['related_books'] = related_books
        return context


class PreviewBookDetailView(DetailView):
    """
    Vista previa del usuario author de la publicación
    """
    template_name = "book_detail.html"
    model = Book

    def get_context_data(self, **kwargs):
        context = super(PreviewBookDetailView, self).get_context_data(**kwargs)
        actual_book = context['book']  # Post consultado
        # Obtenemos los post relacionados
        if self.request.user == actual_book.author or self.request.user.is_superuser:
            cache_categories = cache.get('pythonizame_book_categories')
            if cache_categories:
                context['categories'] = cache_categories
            else:
                context['categories'] = BookCategory.objects.all()
                cache.set('pythonizame_book_categories', 60 * 5)  # Cache por 15 mins
            if actual_book.tags.all():
                related_books = Book.objects.filter(published=True,
                                                    categories=actual_book.categories.all(),
                                                    ).exclude(id=actual_book.id).distinct().order_by('?')[:5]
            else:
                related_books = Book.objects.filter(published=True,
                                                    categories=actual_book.categories.all()
                                                    ).exclude(id=actual_book.id).distinct().order_by('?')[:2]
            context['related_books'] = related_books
            return context
        else:
            raise Http404()
