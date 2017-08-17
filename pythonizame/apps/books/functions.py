__author__ = 'alex'
from .models import Book
from django.db.models import Q


def book_search(raw_text):
    """
    Cortamos el texto y buscamos en la base de datos.
    :param raw_text:
    :return:
    """
    word_list = raw_text.split(' ')
    q = Q(description__icontains=word_list[0]) | Q(title__icontains=word_list[0])
    for term in word_list[1:]:
        q.add((Q(description__icontains=term) | Q(title__icontains=term)), q.connector)
    queryset = Book.objects.filter(Q(published=True), q)
    return queryset
