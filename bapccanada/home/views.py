from django.contrib.auth.forms import AuthenticationForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.http import JsonResponse

from build.models import Build
from home.models import Price
from products.models import Component, Review
from .constants import FRONT_END_URLS


class HomeView(TemplateView):
    template_name = 'home.html'
    oDeals = [
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        },
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        }
        ,
        {
            "cheapest_price": 584.99,
            "current_price": 512.99,
            "component": "ASUS GeForce GTX 1080 8GB ROG STRIX Graphics Card",
        }
    ]
    navComponents = {
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
        "memory": {
            "name": "Memory",
            "url": reverse_lazy('products:ram'),
            "img": static('assets/icons/memory.png')
        },
        "motherboard": {
            "name": "Motherboard",
            "url": reverse_lazy('products:motherboard'),
            "img": static('assets/icons/motherboard.png')
        },
        "power_supply": {
            "name": "Power Supply",
            "url": reverse_lazy('products:power_supply'),
            "img": static('assets/icons/power_supply.png')
        },
        "storage": {
            "name": "Storage",
            "url": reverse_lazy('products:storage'),
            "img": static('assets/icons/storage.png')
        },
        "case": {
            "name": "Case",
            "url": reverse_lazy('products:case'),
            "img": static('assets/icons/case.png')
        },
        "cooler": {
            "name": "Cooler",
            "url": reverse_lazy('products:cooler'),
            "img": static('assets/icons/cooler.png')
        }

    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navComponents'] = self.navComponents
        context['deals'] = self.prepare_deal_info(Component.objects.all()[:10])
        context['builds'] = Build.objects.filter(complete=True).order_by('date_published')[:3]
        return context

    def prepare_deal_info(self, components):
        feature_array = []
        for comp in components:
            feature_array.append({
                "cheapest_price": comp.cheapest_price,
                "current_price": comp.price_set.all()[0].get_price_range(comp.get_polymorphic_class_id())['min'],
                "component": comp.display_title,
                "image_link": comp.get_component_images().first().image_link,
                "component_link": "/products/" + comp.get_actual_class_string() + "/" + comp.slug
            })
        return feature_array


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
