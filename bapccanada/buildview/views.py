from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View

from build.models import Build, CurrentBuild


class Create(View):
    def render(self, request):
        return render(request, 'create.html', {'title': self.title, 'build': self.build,
                                               'component_list': self.component_list})

    def get(self, request, *args, **kwargs):
        if 'shortcode' in kwargs:
            build = get_object_or_404(Build, shortcode=kwargs['shortcode'])
            if request.user.is_authenticated:
                currentBuild = CurrentBuild.objects.get(tracked_user=request.user.userprofile)
                currentBuild.tracked_build = build
                currentBuild.save()

            else:
                currentBuild = Build.objects.get(shortcode=kwargs['shortcode'])
                self.build = currentBuild
                # currentBuild = CurrentBuild.objects.all()[0]
                # currentBuild.tracked_build = build

            print(currentBuild.tracked_user.user.username)
            print(currentBuild.tracked_build.name)

            currentBuild.save()
        self.title = "Current Part List"
        self.build = Build.handle_build_tracking(request)
        self.component_list = self.build.get_component_dict()

        return self.render(request)