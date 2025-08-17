from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   
   TYPE_CHOICE=[
       ("customer","Customer"),
       ("business","Business")
   ]
   type= models.CharField(max_length=8, choices=TYPE_CHOICE,default="customer")