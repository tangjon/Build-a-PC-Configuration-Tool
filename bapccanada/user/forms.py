from django import forms

from django.contrib.auth.models import User

from user.models import UserProfile, ClickSettings, PrivacySettings, EmailSettings


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class BiographyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['biography']


class ClickSettingsForm(forms.ModelForm):
    class Meta:
        model = ClickSettings
        fields = ['links_as_new_window']
        labels = {
            'links_as_new_window': 'open links as a new window'
        }


class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = ['data_for_research', 'index_profile']
        labels = {
            'data_for_research': "allow my data to be used for research purposes",
            'index_profile': "don't allow search engines to index my user profile"
        }


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = ['messeges_as_emails', 'send_email_digest', 'unsubscribe_from_all_emails']
