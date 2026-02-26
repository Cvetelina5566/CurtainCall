from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from theatres.models.theatre import Theatre
from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model for curtaincall
    """

    class Role(models.TextChoices):
        USER = "user", "User"
        THEATER_MANAGER = "theater_manager", "Theater Manager"
        SUPERADMIN = "superadmin", "SuperAdmin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None
    email = EmailField(_("email address"), unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.id})


class UserType(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("theater_manager", "Theater Manager"),
        ("superadmin", "SuperAdmin"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    role_type = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
    )

    theater = models.ForeignKey(
        Theatre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managers",
    )

    def __str__(self):
        return f"{self.user.email} - {self.role_type}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Only create UserType if it doesn't exist
            UserType.objects.get_or_create(
                user=instance,
                defaults={"role_type": instance.role if hasattr(instance, "role") else "user"}
            )
        except Exception as e:
            # Log error but don't fail user creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating UserType for user {instance.email}: {e}")
