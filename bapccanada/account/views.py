from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView

from account.forms import SignUpForm
from user.models import UserProfile
from django.contrib.auth import login as auth_login
from build.models import Build

title = 'User Page'


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            return redirect('home:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'title': 'Login', 'form': form})


class UserCreate(CreateView):
    template_name = 'register.html'
    form_class = SignUpForm

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')
        return redirect('account:sign_up')


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        # must transfer before calling super or request's session id will change
        Build.transfer_anonymous_build(self.request, form.get_user())
        return super(CustomLoginView, self).form_valid(form)


class LogoutView(LogoutView):
    template_name = "logged_out.html"
