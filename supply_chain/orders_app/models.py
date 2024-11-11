from django.db import models

# Create your models here.

class Order_Tb(models.Model):

    BOOK_TITLE = models.CharField(max_length=100)
    BOOK_AUTHOR = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=100)
    BOOK_CATEGORY = models.CharField(max_length=100)
    BOOK_IMAGE = models.ImageField(null =True ,upload_to='outimage/')