from django.db import models
from auth_app.models import User

# Create your models here.


class Profile(models.Model):
    """
    Represents a user profile linked to a User instance.

    Fields:
        user: One-to-one relationship to the User.
        username: Optional username string.
        first_name: Optional first name.
        last_name: Optional last name.
        file: Optional profile picture or file upload.
        location: Optional location string.
        tel: Optional telephone number.
        description: Optional free-text description.
        working_hours: Optional working hours info.
        uploaded_at: Timestamp when profile was created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True, default='') 
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    file = models.FileField(upload_to='profile_pics/', default='', blank=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=50, blank=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"