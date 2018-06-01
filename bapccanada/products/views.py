from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import GPU, CPU, Monitor, Component


def gpu(request):
    gpu_list = GPU.objects.all()[:50]
    dimensions = gpu_list[0].get_filterable_dimensions(GPU)
    return render(request, 'gpuBrowse.html', {'title': 'Choose a Video Card', 'components': gpu_list,
                                              'rating_range': range(1, 6), 'dimensions': dimensions})


def monitors(request):
    return render(request, 'componentDetails.html', {'title': 'Choose a Video Card', 'slug': 'user',
                                            'rating_range': range(1, 6)})


def cpu(request):
    cpu_list = CPU.objects.all()[:50]
    dimensions = cpu_list[0].get_filterable_dimensions(CPU)
    return render(request, 'cpuBrowse.html', {'title': 'Choose a Processor', 'components': cpu_list,
                                              'rating_range': range(1, 6), 'dimensions': dimensions})


def monitor(request):
    monitor_list = Monitor.objects.all()[:50]
    dimensions = monitor_list[0].get_filterable_dimensions(Monitor)
    return render(request, 'monitorBrowse.html', {'title': 'Choose a Monitor', 'components': monitor_list,
                                                  'rating_range': range(1, 6), 'dimensions': dimensions})


def abstract_details(request, slug, category):
    component = get_object_or_404(Component, slug=slug)
    images = component.get_component_images()
    prices = component.get_component_prices()
    tech_details = component.get_tech_details()
    reviews = component.get_component_reviews()
    return render(request, 'componentDetails.html', {'component': component, 'rating_range': range(1, 6),
                                                     'images': images, 'tech_details': tech_details,
                                                     'prices': prices, 'reviews': reviews, 'category': category})


def gpu_detail(request, slug):
    return abstract_details(request, slug, "VIDEO_CARD")


def cpu_detail(request, slug):
    return abstract_details(request, slug, "PROCESSOR")


def monitor_detail(request, slug):
    return abstract_details(request, slug, "MONITOR")
