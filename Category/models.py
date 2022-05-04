from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=5000)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return str(self.id)+"-" + self.name
