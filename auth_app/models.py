from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds a 'type' field to distinguish between customer and business users.
    """

    TYPE_CHOICE = [
        ("customer", "Customer"),
        ("business", "Business")
    ]
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICE,
        default="customer"
    )
    """Defines the role of the user: either 'customer' or 'business'."""