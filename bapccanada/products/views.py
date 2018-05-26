from django.shortcuts import render
from .models import GPU, CPU


def gpu(request):
    gpu_list = GPU.objects.all()[:50]
    return render(request, 'gpuBrowse.html', {'title': 'Choose a Video Card', 'components': gpu_list})


def monitors(request):
    return render(request, 'monitor.html', {'title': 'Choose a Video Card', 'slug': 'user'})


def cpu(request):
    cpu_list = CPU.objects.all()[:50]
    return render(request, 'cpuBrowse.html', {'title': 'Choose a Video Card', 'components': cpu_list})


def monitor(request):
    return render(request, 'monitor.html', {'title': 'Choose a Video Card', 'slug': 'user'})
# Create your views here.
