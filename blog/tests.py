from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase

from .models import Category, Post, Tag


User = get_user_model()


class AuthorDashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="author", password="strongpassword123")
        self.other_user = User.objects.create_user(username="other", password="strongpassword123")
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.tag = Tag.objects.create(name="Django", slug="django")
        self.post = Post.objects.create(
            title="My first post",
            slug="my-first-post",
            author=self.user,
            category=self.category,
            content="Hello world",
            status=Post.Status.DRAFT,
        )
        self.post.tags.add(self.tag)
        self.client.force_authenticate(user=self.user)

    def test_dashboard_returns_user_post_summary(self):
        response = self.client.get(reverse("my-post-dashboard"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_posts"], 1)
        self.assertEqual(response.data["published_posts"], 0)
        self.assertEqual(response.data["draft_posts"], 1)

    def test_author_can_create_and_list_only_their_posts(self):
        create_response = self.client.post(
            reverse("my-post-list"),
            {
                "title": "New post",
                "slug": "new-post",
                "content": "Body",
                "status": Post.Status.PUBLISHED,
                "category": self.category.slug,
                "tags": [self.tag.slug],
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        list_response = self.client.get(reverse("my-post-list"))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["results"][0]["title"], "New post")
from django.contrib.auth import get_user_model

from .models import Category, Post


class CategoryPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username="adminuser", password="strongpassword123")
        self.admin_user.profile.role = "admin"
        self.admin_user.profile.save()

        self.non_admin_user = User.objects.create_user(username="reader", password="strongpassword123")
        self.non_admin_user.profile.role = "reader"
        self.non_admin_user.profile.save()

    def test_non_admin_cannot_create_category(self):
        self.client.force_authenticate(user=self.non_admin_user)
        response = self.client.post(
            reverse("category-list"),
            {"name": "Science", "slug": "science"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_category(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            reverse("category-list"),
            {"name": "Science", "slug": "science"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BlogModelTests(TestCase):
    def test_category_str_and_slug(self):
        category = Category.objects.create(name="Tech")
        self.assertEqual(str(category), "Tech")
        self.assertEqual(category.slug, "tech")

    def test_post_str_and_slug(self):
        user = get_user_model().objects.create_user(username="testuser", password="pass")
        post = Post.objects.create(
            title="Hello World",
            author=user,
            content="Content for the first blog post.",
            status=Post.Status.PUBLISHED,
        )
        self.assertEqual(str(post), "Hello World")
        self.assertEqual(post.slug, "hello-world")
