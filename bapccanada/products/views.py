from django.shortcuts import render
from .models import GPU, CPU, Monitor


def gpu(request):
    gpu_list = GPU.objects.all()[:50]
    return render(request, 'gpuBrowse.html', {'title': 'Choose a Video Card', 'components': gpu_list,
                                              'rating_range': range(1, 6)})


def monitors(request):
    return render(request, 'monitor.html', {'title': 'Choose a Video Card', 'slug': 'user',
                                            'rating_range': range(1, 6)})


def cpu(request):
    cpu_list = CPU.objects.all()[:50]
    return render(request, 'cpuBrowse.html', {'title': 'Choose a Processor', 'components': cpu_list,
                                              'rating_range': range(1, 6)})


def monitor(request):
    monitor_list = Monitor.objects.all()[:50]
    return render(request, 'monitorBrowse.html', {'title': 'Choose a Monitor', 'components': monitor_list,
                                                  'rating_range': range(1, 6)})
# Create your views here.
