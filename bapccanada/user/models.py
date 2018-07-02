from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=False)
    # extra
    biography = models.TextField(blank=True, max_length=300)
    avatar_url = models.URLField(default="", max_length=1000)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'


class ClickSettings(models.Model):
    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    links_as_new_window = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Click Option'


class EmailSettings(models.Model):
    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    messeges_as_emails = models.BooleanField(default=False)
    unsubscribe_from_all_emails = models.BooleanField(default=False)
    send_email_digest = models.BooleanField(default=False)


class PrivacySettings(models.Model):
    profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    data_for_research = models.BooleanField(default=False)
    index_profile = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Privacy Option'
