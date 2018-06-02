from django.shortcuts import render


from . import constants

from .models import Build


def create(request):
    component_list = constants.get_components()
    build = Build.objects.get(pk=2)
    return render(request, 'create.html', {'title': 'Current Part List', 'build': build,
                                           'component_list': component_list})
# Create your views here.
