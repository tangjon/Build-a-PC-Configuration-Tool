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

    class Meta:
        verbose_name = 'Profile'


class UserPreferences(models.Model):
    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return self.profile.user.username

    class Meta:
        verbose_name = 'Preference'


class ClickOptions(models.Model):
    profile = models.OneToOneField(
        UserPreferences,
        on_delete=models.CASCADE,
        primary_key=True
    )
    links_as_new_window = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Click Option'


class PrivacyOptions(models.Model):
    profile = models.OneToOneField(
        UserPreferences,
        on_delete=models.CASCADE,
        primary_key=True
    )
    data_for_research = models.BooleanField(default=False)
    index_profile = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Privacy Option'
