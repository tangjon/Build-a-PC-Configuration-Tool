from django.urls import re_path, path

from . import views

app_name = 'home'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('login/', views.login, name="login")
]
