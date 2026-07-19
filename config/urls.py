from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from blog.feeds import LatestPostsFeed
from blog.sitemaps import PostSitemap, CategorySitemap

sitemaps = {"posts": PostSitemap, "categories": CategorySitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("blog.urls")),
    path("api/auth/", include("users.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("rss/", LatestPostsFeed(), name="rss-feed"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django-sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
