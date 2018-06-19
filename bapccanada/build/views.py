from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from django.http import JsonResponse

from .models import Build, CurrentBuild
from home.constants import FRONT_END_URLS
from products.models import Component


class Create(View):
    def render(self, request):
        return render(request, 'create.html', {'title': self.title, 'build': self.build,
                                               'component_list': self.component_list})

    def get(self, request, *args, **kwargs):
        self.title = "Current Part List"
        self.build = Build.handle_build_tracking(request)
        self.component_list = self.build.get_component_dict()

        return self.render(request)


def change_component(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        action = request.POST.get('action')
        component = get_object_or_404(Component, slug=slug)
        build = Build.handle_build_tracking(request)

        if action == 'add':
            build.modify_component(component, "add")
        else:
            build.modify_component(component, "remove")

        data = {
            "redirect": FRONT_END_URLS["BUILD"]
        }

        return JsonResponse(data)


def save_build(request):
    if request.method == 'POST' and request.POST.get('action') == 'save':
        desired_name = request.POST.get('build_name')

        if desired_name == "":
            return JsonResponse({
                "error": "Name cannot be empty"
            })

        current_build = Build.handle_build_tracking(request)
        current_build.name = desired_name

        # makes a clone of our current_build and saves it with new name
        current_build.pk = None
        current_build.shortcode = ""
        current_build.save()
        data = {
            "saved_name": desired_name,
            "was_added": True,
            "redirect": reverse_lazy('user:builds_show', kwargs={
                'username': request.user.username,
                'pk': current_build.pk
            })
        }

        return JsonResponse(data)

    return JsonResponse("Not a valid save request")


def new_build(request):
    if request.method == 'POST' and request.POST.get('action') == 'new':
        if not request.user.is_authenticated:  # user is not authenticated
            session_key = request.session.session_key
            build_to_reuse = Build.objects.filter(anonymous_session=session_key).first()
            build_to_reuse.clean_build()
        else:
            if not request.user.userprofile.currentbuild.tracked_build.is_pristine():
                created_build = Build.objects.create(owner=request.user.userprofile)
                build_tracker = CurrentBuild.objects.filter(tracked_user=request.user.userprofile).first()
                build_tracker.tracked_build = created_build
                build_tracker.save()

    return JsonResponse({
        "redirect": FRONT_END_URLS["BUILD"]
    })
