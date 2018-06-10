from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import GPU, CPU, Monitor, Component
from home.models import Price


class AbstractComponentBrowseView(ListView):
    context_object_name = "components"
    title = None

    def get_queryset(self):
        # for now just return first 50 until we implement paging
        return self.model.objects.all()[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.title
        context['rating_range'] = range(1, 6)
        context['dimensions'] = context['components'][0].get_filter_metadata_for_manager(self.model)
        context['price_range'] = Price.get_price_range(context['components'][0].get_polymorphic_class_id())

        return context


class GPUBrowseView(AbstractComponentBrowseView):
    model = GPU
    template_name = 'gpuBrowse.html'
    title = 'Choose a Video Card'


class CPUBrowseView(AbstractComponentBrowseView):
    model = CPU
    template_name = 'cpuBrowse.html'
    title = 'Choose a Processor'


class MonitorBrowseView(AbstractComponentBrowseView):
    model = Monitor
    template_name = 'monitorBrowse.html'
    title = 'Choose a Monitor'


class AbstractComponentDetailView(DetailView):
    template_name = 'componentDetails.html'
    context_object_name = "component"
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = self.get_object()

        context['rating_range'] = range(1,6)
        context['images'] = component.get_component_images()
        context['tech_details'] = component.get_tech_details()
        context['reviews'] = component.get_component_reviews()
        context['prices'] = component.get_component_prices()
        context['category'] = self.category

        return context


class GPUDetailView(AbstractComponentDetailView):
    model = GPU
    category = "Video Card"


class CPUDetailView(AbstractComponentDetailView):
    model = CPU
    category = "Processor"


class MonitorDetailView(AbstractComponentDetailView):
    model = Monitor
    category = "Monitor"

