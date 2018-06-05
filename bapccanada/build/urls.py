from django.urls import re_path, path

from . import views

app_name = 'build'
urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('add/', views.change_component, name='add'),
    path('save/', views.save_build, name='save_build')
]
