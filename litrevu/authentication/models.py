from django.contrib.auth.models import AbstractUser
from django.db import models

from litrevu.constants import USER_ROLE


class User(AbstractUser):
    """User model"""
    ADMIN = 'admin'
    SUBSCRIBER = 'subscriber'

    ROLE_CHOICES = (
        (ADMIN, USER_ROLE['r_admin']),
        (SUBSCRIBER, USER_ROLE['r_subscriber']),
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=SUBSCRIBER,
        verbose_name="Rôle")
