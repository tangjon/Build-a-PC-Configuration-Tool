from django import forms

from django.contrib.auth.models import User

from user.models import UserProfile


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class BiographyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['biography']
