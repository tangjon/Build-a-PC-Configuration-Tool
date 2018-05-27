from django import forms

from django.contrib.auth.models import User

from user.models import UserProfile, ClickOptions, PrivacyOptions


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class BiographyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['biography']


class PreferencesClickOptionsForm(forms.ModelForm):
    class Meta:
        model = ClickOptions
        fields = ['links_as_new_window']


class PreferencesClickOptionsForm(forms.ModelForm):
    class Meta:
        model = PrivacyOptions
        fields = ['data_for_research', 'index_profile']
