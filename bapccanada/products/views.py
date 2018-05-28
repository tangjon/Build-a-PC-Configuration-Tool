from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import GPU, CPU, Monitor


def gpu(request):
    gpu_list = GPU.objects.all()[:50]
    return render(request, 'gpuBrowse.html', {'title': 'Choose a Video Card', 'components': gpu_list,
                                              'rating_range': range(1, 6)})


def monitors(request):
    return render(request, 'monitorDetails.html', {'title': 'Choose a Video Card', 'slug': 'user',
                                            'rating_range': range(1, 6)})


def cpu(request):
    cpu_list = CPU.objects.all()[:50]
    return render(request, 'cpuBrowse.html', {'title': 'Choose a Processor', 'components': cpu_list,
                                              'rating_range': range(1, 6)})


def monitor(request):
    monitor_list = Monitor.objects.all()[:50]
    return render(request, 'monitorBrowse.html', {'title': 'Choose a Monitor', 'components': monitor_list,
                                                  'rating_range': range(1, 6)})


def gpu_detail(request, slug):
    component = get_object_or_404(GPU, slug=slug)
    images = component.get_component_images()

    return render(request, 'monitorDetails.html', {'component': component, 'rating_range': range(1, 6),
                                                   'images': images})


def cpu_detail(request, slug):
    component = get_object_or_404(CPU, slug=slug)
    images = component.get_component_images()
    return render(request, 'cpuDetails.html', {'component': component, 'rating_range': range(1, 6),
                                               'images': images})


def monitor_detail(request, slug):
    component = get_object_or_404(Monitor, slug=slug)
    images = component.get_component_images()
    return render(request, 'monitorDetails.html', {'component': component, 'rating_range': range(1, 6),
                                                   'images': images})
