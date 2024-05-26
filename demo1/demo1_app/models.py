from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Resource(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.name