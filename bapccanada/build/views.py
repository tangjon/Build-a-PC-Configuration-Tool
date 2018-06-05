from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse

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


def change_component(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        action = request.POST.get('action')
        component = get_object_or_404(Component, slug=slug)
        build = get_object_or_404(Build, pk=999)

        if action == 'add':
            build.add_component(component)
        else:
            build.remove_component(component)

        data = {
            "redirect": "/build"
        }

        return JsonResponse(data)


def save_build(request):
    if request.method == 'POST' and request.POST.get('action') == 'save':
        desired_name = request.POST.get('build_name')

        if desired_name == "":
            return JsonResponse({
                "error": "Name cannot be empty"
            })

        current_build = get_object_or_404(Build, pk=999)
        current_build.name = desired_name
        current_build.save()

        data = {
            "was_added": True
        }

        return JsonResponse(data)

    return JsonResponse("Not a valid save request")