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
    re_path(r'^memory/(?P<slug>[-\w]+)/$', views.MemoryDetailView.as_view(), name='ram_detail'),
    path('motherboard/', views.MotherboardBrowseView.as_view(), name='motherboard'),
    re_path(r'^motherboard/(?P<slug>[-\w]+)/$', views.MotherboardDetailView.as_view(), name='motherboard_detail'),
    path('powersupply/', views.PowerSupplyBrowseView.as_view(), name='power_supply'),
    re_path(r'^powersupply/(?P<slug>[-\w]+)/$', views.PowerSupplyDetailView.as_view(), name='power_supply_detail'),
    path('storage/', views.StorageBrowseView.as_view(), name='storage'),
    re_path(r'^storage/(?P<slug>[-\w]+)/$', views.StorageDetailView.as_view(), name='storage_detail'),
    path('case/', views.CaseBrowseView.as_view(), name='case'),
    re_path(r'^case/(?P<slug>[-\w]+)/$', views.CaseDetailView.as_view(), name='case_detail'),
    path('cooler/', views.CoolerBrowseView.as_view(), name='cooler'),
    re_path(r'^cooler/(?P<slug>[-\w]+)/$', views.CoolerDetailView.as_view(), name='cooler_detail')
]
