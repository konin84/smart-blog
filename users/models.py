from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("editor", "Editor"),
        ("author", "Author"),
        ("reader", "Reader"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="reader")
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
