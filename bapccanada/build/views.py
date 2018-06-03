from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .models import Build
from products.models import Component


class Create(View):
    def render(self, request):
        return render(request, 'create.html', {'title': self.title, 'build': self.build,
                                               'component_list': self.component_list})

    def get(self, request):
        self.title = "Current Part List"
        self.build = Build.objects.get(pk=999)
        self.component_list = self.build.get_component_dict()

        return self.render(request)


class AddComponent(View):
    def get(self, request, slug):
        component = get_object_or_404(Component, slug=slug)
        build = get_object_or_404(Build, pk=999)
        build.add_component(component)
        return redirect('build:create')


class RemoveComponent(View):
    def get(self, request, slug):
        component = get_object_or_404(Component, slug=slug)
        build = get_object_or_404(Build, pk=999)
        build.remove_component(component)
        return redirect('build:create')
