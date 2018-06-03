from django.urls import re_path, path

from . import views

app_name = 'build'
urlpatterns = [
    path('', views.Create.as_view(), name='create'),
]
