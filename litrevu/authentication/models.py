from django.contrib.auth.models import AbstractUser
from django.db import models

from litrevu.constants import USER_ROLE


class User(AbstractUser):
    """User model"""
    pass
