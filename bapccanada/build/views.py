from django.shortcuts import render
from django.views.generic import View

from .models import Build


class Create(View):
    def render(self, request):
        return render(request, 'create.html', {'title': self.title, 'build': self.build,
                                               'component_list': self.component_list})

    def get(self, request):
        self.title = "Current Part List"
        self.build = Build.objects.get(pk=2)
        self.component_list = self.build.get_component_dict()

        return self.render(request)