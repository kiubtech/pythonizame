__author__ = 'alex'
from .models import Post
from django.db.models import Q


def blog_search(raw_text):
    """
    Cortamos el texto y buscamos en la base de datos.
    :param raw_text:
    :return:
    """
    word_list = raw_text.split(' ')
    q = Q(content__icontains=word_list[0]) | Q(title__icontains=word_list[0])
    for term in word_list[1:]:
        q.add((Q(content__icontains=term) | Q(title__icontains=term)), q.connector)
    queryset = Post.objects.filter(Q(published=True), q)
    return queryset
