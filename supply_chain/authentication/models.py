from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    NAME = models.CharField(max_length=50)
    CONTACT = models.CharField(max_length=15)
    AGE = models.IntegerField(default=0)
    GENDER = models.CharField(max_length=20)
    