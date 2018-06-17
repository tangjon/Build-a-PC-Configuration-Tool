from django.urls import re_path, path

from . import views

app_name = 'build'
urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    re_path(r'^(?P<shortcode>\w+)/$', views.Create.as_view(), name='create_shortcode'),
    path('change/', views.change_component, name='change'),
    path('save/', views.save_build, name='save_build'),
    path('new/', views.new_build, name='new_build')
]
