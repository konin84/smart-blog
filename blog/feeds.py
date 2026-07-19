from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Blog — latest posts"
    link = "/"
    description = "Latest published posts."

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.content[:200]

    def item_link(self, item):
        return f"/posts/{item.slug}/"

    def item_pubdate(self, item):
        return item.published_at
