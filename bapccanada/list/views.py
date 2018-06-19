from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View

from build.models import Build, CurrentBuild


class Create(View):
    def render(self, request):
        return render(request, 'view.html', {'title': self.title, 'build': self.build,
                                               'component_list': self.component_list})

    def get(self, request, *args, **kwargs):
        self.title = "View Part List"
        if 'shortcode' in kwargs:
            self.build = get_object_or_404(Build, shortcode=kwargs['shortcode'])
            self.component_list = self.build.get_component_dict()
            if request.user.is_authenticated:
                # Change tracking build
                currentBuild = CurrentBuild.objects.get(tracked_user=request.user.userprofile)
                currentBuild.tracked_build = self.build
                currentBuild.save()
            return self.render(request)
        else:
            raise Http404()
