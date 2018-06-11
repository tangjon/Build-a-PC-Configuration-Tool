from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse

from build.models import Build
from products.models import Component, Review
from .constants import FRONT_END_URLS


class HomeView(TemplateView):
    template_name = 'home.html'
    data = {
        "0": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "1": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "2": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "3": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "4": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "5": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "6": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "7": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        "8": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        }
        ,
        "9": {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        }

    }

    choices = {'key1': 'val1', 'key2': 'val2'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deals'] = self.data
        context['builds'] = Build.objects.all()[:3]
        return context


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
