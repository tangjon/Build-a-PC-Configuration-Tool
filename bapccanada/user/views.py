from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.models import User

from build.models import Build
from products.models import Review
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
        # return super(ProfileView, self).render_to_response(context)

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

    def get_context_data(self, **kwargs):
        context = super(CommentsView, self).get_context_data(**kwargs)
        context['reviews'] = self.browse_user.userprofile.review_set.all()[:10]
        return context


class CommentsDeleteView(DeleteView):
    model = Review
    template_name = 'comments_delete.html'
    success_url = reverse_lazy('user:comments')

    def get_success_url(self):
        return reverse('user:comments', kwargs={'username': self.kwargs['username']})


class BuildsView(BaseProfileView):
    template_name = 'builds.html'
    title_name = 'Builds'

    # def get(self, request, *args, **kwargs):
    #     super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(BuildsView, self).get_context_data(**kwargs)
        context['builds'] = self.browse_user.userprofile.build_set.all()
        if context['builds'].count():
            if 'pk' in kwargs:
                context['build'] = get_object_or_404(self.browse_user.userprofile.build_set, pk=kwargs['pk'])
                context['component_list'] = Build.get_component_dict(context['build'])

            else:
                context['build'] = self.browse_user.userprofile.build_set.first()
                context['component_list'] = Build.get_component_dict(context['build'])
        return context


class SecurityView(LoginRequiredMixin, BaseProfileView):
    template_name = 'security.html'
    title_name = 'Security'
    login_url = reverse_lazy('account:login')

    def get_context_data(self, **kwargs):
        context = super(SecurityView, self).get_context_data(**kwargs)
        context['change_password_form'] = PasswordChangeForm(context['browse_user'])
        return context

    def post(self, request, *args, **kwargs):
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important!
        return self.get(request, *args, **kwargs)


class SavedView(BaseProfileView):
    template_name = 'saved.html'
    title_name = 'Saved Parts'
