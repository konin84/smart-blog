from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "category", "author", "published_at"]
    list_filter = ["status", "category", "tags"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ["title"]}
    filter_horizontal = ["tags"]
    date_hierarchy = "published_at"
