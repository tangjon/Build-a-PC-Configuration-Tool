from django.contrib.auth.forms import AuthenticationForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.http import JsonResponse

from build.models import Build
from products.models import Component, Review
from .constants import FRONT_END_URLS


class HomeView(TemplateView):
    template_name = 'home.html'
    oDeals = {
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

    components = {
        "cpu": {
            "name": "CPU",
            "url": reverse_lazy('products:cpu'),
            "img": static('assets/icons/cpu.png')
        },
        "gpu": {
            "name": "GPU",
            "url": reverse_lazy('products:gpu'),
            "img": static('assets/icons/gpu.png')
        },
        "monitor": {
            "name": "Monitor",
            "url": reverse_lazy('products:monitors'),
            "img": static('assets/icons/monitor.png')
        },

    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deals'] = self.oDeals
        context['components'] = self.components
        context['builds'] = Build.objects.all().order_by('points')[:3]
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
