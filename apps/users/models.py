from django.db import models

from apps.authentication.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=150, null=True, blank=True)
    last_name = models.CharField('last name', max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        app_label = 'users'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
