from django.urls import re_path, path

from . import views

app_name = 'products'
urlpatterns = [
    path('gpu/', views.GPUBrowseView.as_view(), name='gpu'),
    re_path(r'^gpu/(?P<slug>[-\w]+)/$', views.GPUDetailView.as_view(), name='gpu_detail'),
    path('cpu/', views.CPUBrowseView.as_view(), name='cpu'),
    re_path(r'^cpu/(?P<slug>[-\w]+)/$', views.CPUDetailView.as_view(), name='cpu_detail'),
    path('monitor/', views.MonitorBrowseView.as_view(), name='monitors'),
    re_path(r'^monitor/(?P<slug>[-\w]+)/$', views.MonitorDetailView.as_view(), name='monitor_detail'),
    path('memory/', views.MemoryBrowseView.as_view(), name='ram'),
    re_path(r'^memory/(?P<slug>[-\w]+)/$', views.MemoryDetailView.as_view(), name='ram_detail')
]
