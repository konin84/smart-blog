from django.db.models import Q
from rest_framework import filters, permissions, viewsets

from users.models import UserProfile
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Category, Tag
from .serializers import (
    AuthorPostSerializer,
    AuthorPostWriteSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CategorySerializer,
    TagSerializer,
)


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/posts/                -> list, paginated
    /api/posts/?category=tech  -> filter by category slug
    /api/posts/?tag=django     -> filter by tag slug
    /api/posts/?search=foo     -> full text search (title, excerpt, content)
    /api/posts/<slug>/         -> detail (lookup by slug, not id)
    """
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED).select_related(
        "author", "category"
    ).prefetch_related("tags")
    pagination_class = StandardPagination
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "excerpt", "content"]
    ordering_fields = ["published_at", "title"]

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == "retrieve" else PostListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")
        if category:
            qs = qs.filter(category__slug=category)
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs.distinct()


class AuthorPostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related("category").prefetch_related("tags")

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            return AuthorPostWriteSerializer
        return AuthorPostSerializer

    @action(detail=False, methods=["get"])
    def dashboard(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_posts = queryset.count()
        published_posts = queryset.filter(status=Post.Status.PUBLISHED).count()
        draft_posts = queryset.filter(status=Post.Status.DRAFT).count()
        return Response(
            {
                "total_posts": total_posts,
                "published_posts": published_posts,
                "draft_posts": draft_posts,
            }
        )


class RelatedPostsMixin:
    """Helper used by the frontend detail page: same category, excluding current post."""
    pass


def related_posts(post, limit=3):
    qs = Post.objects.filter(status=Post.Status.PUBLISHED).exclude(id=post.id)
    if post.category_id:
        qs = qs.filter(category_id=post.category_id)
    return qs[:limit]


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == "admin")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.AllowAny()]
        return [IsAdminRole()]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
