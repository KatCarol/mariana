from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_1 = models.CharField(max_length=15, null=True)
    phone_2 = models.CharField(max_length=15, null=True, blank=True)