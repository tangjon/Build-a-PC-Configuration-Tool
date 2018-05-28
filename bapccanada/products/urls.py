from django.urls import re_path, path

from . import views

app_name = 'products'
urlpatterns = [
    path('gpu/', views.gpu, name='gpu'),
    re_path(r'^gpu/(?P<slug>[-\w]+)/$', views.gpu_detail, name='gpu_detail'),
    path('cpu/', views.cpu, name='cpu'),
    re_path(r'^cpu/(?P<slug>[-\w]+)/$', views.cpu_detail, name='cpu_detail'),
    path('monitor/', views.monitor, name='monitors'),
    re_path(r'^monitor/(?P<slug>[-\w]+)/$', views.monitor_detail, name='monitor_detail'),
    path('gpu/monitor', views.monitors, name='monitor')
]
