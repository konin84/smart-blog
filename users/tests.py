from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import UserProfile


User = get_user_model()


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("register")

    def test_register_user(self):
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpassword123",
            "password_confirm": "strongpassword123",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["email"], "new@example.com")


class UserProfileTests(TestCase):
    def test_new_user_gets_profile_with_default_role(self):
        user = User.objects.create_user(username="profileuser", password="strongpassword123")

        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.role, "reader")


class UserSeederTests(TestCase):
    def test_seed_users_creates_expected_accounts(self):
        call_command("seed_users", verbosity=0)

        self.assertTrue(User.objects.filter(username="admin").exists())
        self.assertTrue(User.objects.filter(username="jane").exists())
        self.assertTrue(User.objects.filter(username="john").exists())

        admin_user = User.objects.get(username="admin")
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.check_password("Password123!"))
        self.assertEqual(admin_user.profile.role, "admin")

        regular_users = User.objects.filter(username__in=["jane", "john"])
        self.assertEqual(regular_users.count(), 2)
        self.assertTrue(all(user.check_password("Password123!") for user in regular_users))
        self.assertEqual(regular_users.get(username="jane").profile.role, "editor")
        self.assertEqual(regular_users.get(username="john").profile.role, "author")


class UserProfileAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="profileapi", password="strongpassword123")
        self.url = reverse("user-detail")

    def test_user_can_update_profile(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "first_name": "Ada",
            "profile": {
                "bio": "Writer and engineer",
                "location": "London",
                "role": "author",
            },
        }

        response = self.client.patch(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Ada")
        self.assertEqual(response.data["profile"]["bio"], "Writer and engineer")
        self.assertEqual(response.data["profile"]["location"], "London")
        self.assertEqual(response.data["profile"]["role"], "author")


class JWTAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="strongpassword123")
        self.token_url = reverse("token_obtain_pair")
        self.logout_url = reverse("logout")

    def authenticate(self):
        token_response = self.client.post(
            self.token_url,
            {"username": "testuser", "password": "strongpassword123"},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return token_response.data["refresh"]

    def test_logout_invalid_refresh(self):
        self.authenticate()
        response = self.client.post(self.logout_url, {"refresh": "badtoken"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_obtain_and_logout(self):
        refresh = self.authenticate()
        logout_response = self.client.post(self.logout_url, {"refresh": refresh}, format="json")
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)
