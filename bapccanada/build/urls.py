from django.urls import re_path, path

from . import views

app_name = 'build'
urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    re_path(r'^add/(?P<slug>[-\w]+)/$', views.AddComponent.as_view(), name='add_component'),
    re_path(r'^remove/(?P<slug>[-\w]+)/$', views.RemoveComponent.as_view(), name='remove_component')
]
