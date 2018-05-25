from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=False)
    # extra
    biography = models.TextField(blank=True, max_length=300)
    avatar = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.user.username
