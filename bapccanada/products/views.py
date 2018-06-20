from django.views.generic import ListView, DetailView

import json

from .models import GPU, CPU, Monitor, RAM, Motherboard
from .FilterProcessor import FilterProcessor
from home.models import Price


class AbstractComponentBrowseView(ListView):
    context_object_name = "components"
    title = None
    filter_data = None

    def get_queryset(self):
        if self.request.GET.get('filters'):
            self.filter_data = json.loads(self.request.GET.get('filters'))
            filter_processor = FilterProcessor(self.model, self.filter_data)
            return filter_processor.get_filtered_objects()[:50]
        else:
            return self.model.objects.all()[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['rating_range'] = range(1, 6)
        dimension_data = self.model.objects.all().first().get_filter_metadata_for_manager(self.model)
        price_data = Price.get_price_range(self.model.objects.all().first().get_polymorphic_class_id())

        context['dimensions'] = dimension_data

        if not self.filter_data:
            context['filter_metadata'] = json.dumps(dimension_data)
            context['price_range'] = price_data
            context['price_metadata'] = json.dumps(price_data)
        else:
            context['filter_metadata'] = json.dumps(self.filter_data.get('dimensions'))
            context['price_range'] = self.filter_data.get('ranges')
            context['price_metadata'] = json.dumps(self.filter_data.get('ranges'))
            context['rating_metadata'] = json.dumps(self.filter_data.get('ratings'))

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


class MemoryBrowseView(AbstractComponentBrowseView):
    model = RAM
    template_name = 'memoryBrowse.html'
    title = 'Choose memory'


class MotherboardBrowseView(AbstractComponentBrowseView):
    model = Motherboard
    template_name = 'motherboardBrowse.html'
    title = 'Choose a Motherboard'


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


class MemoryDetailView(AbstractComponentDetailView):
    model = RAM
    category = "Memory"


class MotherboardDetailView(AbstractComponentDetailView):
    model = Motherboard
    category = "Motherboard"
