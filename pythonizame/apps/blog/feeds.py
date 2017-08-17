__author__ = 'alex'
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import Post


class LatestEntriesFeed(Feed):
    title = "Noticias sobre el mundo Python"
    link = "/blog/rss/"
    description = "Encuentra todos los días información y noticias del mundo Python"

    def items(self):
        return Post.objects.filter(published=True).order_by('-publication_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])
