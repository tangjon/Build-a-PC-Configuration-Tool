from django.shortcuts import render

from .models import Build


def create(request):
    build = Build.objects.get(pk=999)
    component_list = build.get_component_dict()

    return render(request, 'create.html', {'title': 'Current Part List', 'build': build,
                                           'component_list': component_list})
# Create your views here.
