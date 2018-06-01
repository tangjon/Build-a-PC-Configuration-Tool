from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from user.forms import BiographyForm, AvatarForm, ClickSettingsForm, PrivacySettingsForm, EmailSettingsForm


class BaseProfileView(TemplateView):
    title_name = None
    browse_user = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_name
        context['browse_user'] = self.browse_user
        return context

    def dispatch(self, request, *args, **kwargs):
        self.browse_user = get_object_or_404(User, username=kwargs['username'])
        return super(BaseProfileView, self).dispatch(request, *args, **kwargs)


class ProfileView(BaseProfileView):
    template_name = 'profile.html'
    title_name = 'Profile'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if 'biography' in request.POST:
            context['biography_form'] = BiographyForm(request.POST, instance=context['browse_user'].userprofile)
            if context['biography_form'].is_valid():
                context['biography_form'].save(commit=True)
        if 'avatar' in request.FILES:
            context['avatar_form'] = AvatarForm(files=request.FILES,
                                                instance=context['browse_user'].userprofile)
            if context['avatar_form'].is_valid():
                context['avatar_form'].save(commit=True)
        if 'avatar-clear' in request.POST:
            context['avatar_form'] = AvatarForm(request.POST,
                                                instance=context['browse_user'].userprofile)
            if context['avatar_form'].is_valid():
                context['avatar_form'].save(commit=True)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['biography_form'] = BiographyForm(instance=context['browse_user'].userprofile)
        context['avatar_form'] = AvatarForm(instance=context['browse_user'].userprofile)
        return context


class PreferencesView(BaseProfileView):
    template_name = 'preferences.html'
    title_name = 'Preferences'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        clickSettingsForm = ClickSettingsForm(request.POST, instance=context['browse_user'].userprofile.clicksettings)
        if clickSettingsForm.is_valid():
            clickSettingsForm.save()
        emailSettingsForm = EmailSettingsForm(request.POST, instance=context['browse_user'].userprofile.emailsettings)
        if emailSettingsForm.is_valid():
            emailSettingsForm.save()
        privacySettingsForm = PrivacySettingsForm(request.POST,
                                                  instance=context['browse_user'].userprofile.privacysettings)
        if privacySettingsForm:
            privacySettingsForm.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreferencesView, self).get_context_data(**kwargs)
        context['click_options_form'] = ClickSettingsForm(instance=context['browse_user'].userprofile.clicksettings)
        context['email_options_form'] = EmailSettingsForm(instance=context['browse_user'].userprofile.emailsettings)
        context['privacy_settings_form'] = PrivacySettingsForm(
            instance=context['browse_user'].userprofile.privacysettings)
        return context


class CommentsView(BaseProfileView):
    template_name = 'comments.html'
    title_name = 'Comments'


class BuildsView(BaseProfileView):
    template_name = 'builds.html'
    title_name = 'Builds'


class SecurityView(BaseProfileView):
    template_name = 'security.html'
    title_name = 'Security'


class SavedView(BaseProfileView):
    template_name = 'saved.html'
    title_name = 'Saved Parts'
