from django.shortcuts import render
from .models import GPU


def gpu(request):
    gpu_list = GPU.objects.all()[:50]
    return render(request, 'gpuBrowse.html', {'title': 'Choose a Video Card', 'components': gpu_list})


def monitors(request):
    return render(request, 'monitor.html', {'title': 'Choose a Video Card', 'slug': 'user'})


def cpu(request):
    return render(request, 'monitor.html', {'title': 'Choose a Video Card', 'slug': 'user'})


def monitor(request):
    return render(request, 'monitor.html', {'title': 'Choose a Video Card', 'slug': 'user'})
# Create your views here.
