from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView

from build.models import Build
from products.models import Review
from user.forms import BiographyForm, AvatarForm, ClickSettingsForm, PrivacySettingsForm, EmailSettingsForm, ReviewForm
from user.models import UserProfile


class BaseProfileView(TemplateView):
    title_name = None
    browse_user = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_name
        context['browse_user'] = get_object_or_404(User, username=kwargs['username'])
        return context

    def dispatch(self, request, *args, **kwargs):
        self.browse_user = get_object_or_404(User, username=kwargs['username'])
        return super(BaseProfileView, self).dispatch(request, *args, **kwargs)


class ProfileView(BaseProfileView):
    template_name = 'profile.html'
    title_name = 'Profile'

    def post(self, request, *args, **kwargs):
        if request.user.pk == self.browse_user.pk:
            if 'biography' in request.POST:
                form = BiographyForm(request.POST, instance=request.user.userprofile)
                if form.is_valid():
                    form.save(commit=True)
            if 'avatar' in request.FILES:
                form = AvatarForm(files=request.FILES,
                                  instance=self.request.user.userprofile)
                if form.is_valid():
                    form.save(commit=True)
            if 'avatar-clear' in request.POST:
                form = AvatarForm(request.POST,
                                  instance=self.request.user.userprofile)
                if form.is_valid():
                    form.save(commit=True)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['browse_user_karma'] = context['browse_user'].userprofile.review_set.all().aggregate(Sum('points'))[
            'points__sum']
        context['biography_form'] = BiographyForm(instance=context['browse_user'].userprofile)
        context['avatar_form'] = AvatarForm(instance=context['browse_user'].userprofile)
        return context


class PreferencesView(BaseProfileView):
    template_name = 'preferences.html'
    title_name = 'Preferences'

    def post(self, request, *args, **kwargs):
        if request.user.pk == self.browse_user.pk:
            clickSettingsForm = ClickSettingsForm(request.POST, instance=self.request.user.userprofile.clicksettings)
            if clickSettingsForm.is_valid():
                clickSettingsForm.save()
            emailSettingsForm = EmailSettingsForm(request.POST, instance=self.request.user.userprofile.emailsettings)
            if emailSettingsForm.is_valid():
                emailSettingsForm.save()
            privacySettingsForm = PrivacySettingsForm(request.POST,
                                                      instance=self.request.user.userprofile.privacysettings)
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


class ReviewView(BaseProfileView):
    template_name = 'comments.html'
    title_name = 'Comments'

    def get_context_data(self, **kwargs):
        context = super(ReviewView, self).get_context_data(**kwargs)
        context['reviews'] = context['browse_user'].userprofile.review_set.all()[:10]
        return context


def review_delete(request, **kwargs):
    try:
        review = request.user.userprofile.review_set.get(pk=kwargs['pk'])
    except Review.DoesNotExist:
        raise Http404()
    if request.method == 'POST':
        if review.user.pk == request.user.pk:
            review.delete()
            data = {
                "was_deleted": True,
                "pk": kwargs['pk']
            }
            return JsonResponse(data)
    return Http404()


def review_update(request, **kwargs):
    try:
        review = request.user.userprofile.review_set.get(pk=kwargs['pk'])
    except Review.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        form = ReviewForm(data={
            "content": request.POST['data']
        })
        if form.is_valid():
            review.content = form.cleaned_data['content']
            review.save()
            return JsonResponse({
                "is_updated": True,
                "pk": kwargs['pk'],
                "data": {
                    "content": review.content
                }
            })
    return Http404()


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

            else:  # default to display first build
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
