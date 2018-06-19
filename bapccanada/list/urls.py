from django.urls import re_path, path

from . import views

app_name = "list"

urlpatterns = [
    re_path(r'^(?P<shortcode>\w+)/$', views.Create.as_view(), name='create_shortcode'),
]