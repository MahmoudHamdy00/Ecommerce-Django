from asyncio.windows_events import NULL
from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
import imp
from django.db import models
from Category.models import Category
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=4)
    img = models.ImageField(upload_to='img')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return str(self.id)+"-" + self.name
