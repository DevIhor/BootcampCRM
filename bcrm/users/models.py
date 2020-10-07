from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        app_label = 'users'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
