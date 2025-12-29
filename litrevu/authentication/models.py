from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model"""
    ADMIN = 'admin'
    SUBSCRIBER = 'subscriber'

    ROLE_CHOICES = (
        (ADMIN, 'Administrateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=SUBSCRIBER,
        verbose_name="Rôle")
