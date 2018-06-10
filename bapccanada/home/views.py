from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse

from products.models import Component, Review
from .constants import FRONT_END_URLS


class HomeView(TemplateView):
    template_name = 'home.html'


def home_view(request):
    return render(request, 'home.html', {'title': 'Home'})


def add_review(request):
    if request.user.is_authenticated and request.method == 'POST' and request.POST.get('action') == 'new':
        review_content = request.POST.get('content')
        review_rating = int(request.POST.get('rating'))
        review_slug = request.POST.get('slug')
        component = Component.objects.filter(slug=review_slug).first()

        Review.objects.create(user=request.user.userprofile, content=review_content, component=component,
                              stars=review_rating)

        redirect_url = FRONT_END_URLS["PRODUCTS"] + component.get_actual_class_string() + "/" + review_slug + "/"

        return JsonResponse({
            "was_added": True,
            "redirect": redirect_url
        })
