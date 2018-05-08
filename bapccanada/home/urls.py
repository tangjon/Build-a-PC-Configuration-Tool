from django.urls import re_path, path

from . import views

app_name = 'home'
urlpatterns = [
    re_path(r'^$', views.home_view, name='home'),
    re_path(r'^login/$', views.login_view, name="login"),
    re_path(r'^signup/$', views.signup_view, name='signup')
]
