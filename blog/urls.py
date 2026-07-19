from rest_framework.routers import DefaultRouter
from .views import AuthorPostViewSet, PostViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("my-posts", AuthorPostViewSet, basename="my-post")
router.register("categories", CategoryViewSet, basename="category")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls
