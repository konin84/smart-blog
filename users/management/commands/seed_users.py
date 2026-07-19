from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from users.models import UserProfile


class Command(BaseCommand):
    help = "Create a superuser and two additional users if they do not already exist"

    def handle(self, *args, **options):
        User = get_user_model()
        users = [
            {
                "username": "admin",
                "email": "admin@yopmail.com",
                "password": "Password123!",
                "is_superuser": True,
                "is_staff": True,
                "role": "admin",
            },
            {
                "username": "jane",
                "email": "jane@yopmail.com",
                "password": "Password123!",
                "is_superuser": False,
                "is_staff": False,
                "role": "editor",
            },
            {
                "username": "john",
                "email": "john@yopmail.com",
                "password": "Password123!",
                "is_superuser": False,
                "is_staff": False,
                "role": "author",
            },
        ]

        for user_data in users:
            username = user_data["username"]
            user = User.objects.filter(username=username).first()
            if user is None:
                User.objects.create_user(
                    username=username,
                    email=user_data["email"],
                    password=user_data["password"],
                )
                user = User.objects.get(username=username)

            user.email = user_data["email"]
            user.is_superuser = user_data["is_superuser"]
            user.is_staff = user_data["is_staff"]
            user.save()

            if user_data["password"]:
                user.set_password(user_data["password"])
                user.save()

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = user_data["role"]
            profile.save()

        self.stdout.write(self.style.SUCCESS("Users seeded successfully."))
