from django.contrib.sitemaps import Sitemap
from .models import Post, Category


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/posts/{obj.slug}/"


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f"/category/{obj.slug}/"
