__author__ = 'alex'
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Book


class LatestEntriesFeed(Feed):
    title = "Libros Python"
    link = "/books/rss/"
    description = "Actualización de la integración de nuevos libros al repositorio Pythonízame"

    def items(self):
        return Book.objects.filter(published=True).order_by('-publication_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('books:detail', args=[item.slug])
