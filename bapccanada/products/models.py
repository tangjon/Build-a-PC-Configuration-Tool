from django.db import models
from django.db.models import Min, Avg, Max
from django.template.defaultfilters import slugify

from polymorphic.models import PolymorphicModel

from user.models import UserProfile


class Component(PolymorphicModel):
    manufacturer = models.CharField(max_length=30)
    model_number = models.CharField(max_length=30, blank=True)
    serial_number = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=100, default="")
    display_title = models.CharField(max_length=200, default="")

    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    cheapest_price = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)
    cheapest_price_shipping = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)
    cheapest_price_store_link = models.URLField()
    cheapest_price_store = models.CharField(max_length=100, default="")
    image_thumbnail = models.URLField()

    average_rating = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    num_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.manufacturer, self.model_number)

    def save(self, *args, **kwargs):
        if self.model_number != "":
            self.display_name = "{} {}".format(self.manufacturer, self.model_number)
            self.slug = slugify(self.model_number)
        else:
            self.display_name = "{} {}".format(self.manufacturer, self.serial_number)
            self.slug = slugify(self.serial_number)

        self.slug += "-" + slugify(self.id)
        self.display_title = self.get_page_title()

        super(Component, self).save(*args, **kwargs)

    def update_ratings(self):
        num_ratings = self.review_set.filter(component=self)
        self.num_ratings = num_ratings.count()
        self.average_rating = num_ratings.aggregate(Avg("stars"))["stars__avg"]
        self.save()

    def update_cheapest_pricing(self):
        current_min_price = self.get_component_prices().aggregate(Min('price'))["price__min"]
        if self.cheapest_price == 0.0 or current_min_price <= self.cheapest_price:
            price_to_use = self.get_component_prices().filter(price=current_min_price).first()
            self.cheapest_price = price_to_use.price
            self.cheapest_price_shipping = price_to_use.shipping
            self.cheapest_price_store = price_to_use.store
            self.cheapest_price_store_link = price_to_use.store_link
            self.save()

    def get_actual_class_string(self):
        actual_class = self.get_real_instance_class()

        if actual_class == CPU:
            return "cpu"
        elif actual_class == GPU:
            return "gpu"
        else:
            return "monitor"

    def get_polymorphic_class_id(self):
        return self.polymorphic_ctype_id

    # used for component detail title
    def get_page_title(self):
        pass

    def get_component_reviews(self):
        return self.review_set.order_by('-time_added').filter(component=self)[:10]

    def get_tech_details(self):
        return {
            "Manufacturer": self.manufacturer,
            "Model": self.model_number,
            "Part #": self.serial_number
        }

    def get_filterable_dimensions(self, subtype):
        return {
            "Manufacturer": subtype.objects.order_by('manufacturer').values_list('manufacturer', flat=True).distinct()
        }

    def get_filter_metadata_for_manager(self, subtype):
        filterable_dimensions = self.get_filterable_dimensions(subtype)
        button_id_tracker = 1

        for dimension, values in filterable_dimensions.items():
            # convert each list of values into a format our manager can understand
            converted_values = []
            filterable_dimension_name = self.get_filterable_dimension_name(dimension)

            for value in values:
                converted_values.append({
                    "checkbox_id": button_id_tracker,
                    "filter_value": value,
                    "data_type": type(value).__name__,
                    "filterable_dimension_name": filterable_dimension_name,
                    "was_checked": False
                })

                button_id_tracker += 1

            filterable_dimensions[dimension] = converted_values

        return filterable_dimensions

    def get_component_images(self):
        return self.image_set.all()

    def get_component_prices(self):
        return self.price_set.all()

    def get_filterable_dimension_name(self, ui_dimension_name):
        if ui_dimension_name == "Manufacturer":
            return "manufacturer"
        else:
            return None


class GPU(Component):
    clock_rate = models.DecimalField(default=0.0, max_digits=3, decimal_places=2, blank=True, null=True)
    chipset = models.CharField(max_length=100)
    clock_rate_oc = models.DecimalField(default=0.0, max_digits=3, decimal_places=2, blank=True, null=True)
    memory_size = models.PositiveIntegerField(default=10)
    hdmi_ports = models.PositiveIntegerField(default=0)
    dp_ports = models.PositiveIntegerField(default=0)

    def get_page_title(self):
        return "{} - {} {}GB {} Video Card".format(self.manufacturer, self.chipset,
                                                   self.memory_size, self.model_number)

    def get_tech_details(self):
        main_details = super(GPU, self).get_tech_details()
        extra_details = {
            "Chipset": self.chipset,
            "Memory Size": "{}GB".format(self.memory_size),
            "Base Clock": "{}Ghz".format(self.clock_rate),
            "Boost Clock": "{}Ghz".format(self.clock_rate_oc),
            "Displayport": self.dp_ports,
            "HDMI": self.hdmi_ports
        }

        return {**main_details, **extra_details}

    def get_filterable_dimensions(self, subtype):
        base_dimensions = super(GPU, self).get_filterable_dimensions(subtype)
        extra_dimensions = {
            'chipset': subtype.objects.order_by('chipset').values_list('chipset', flat=True).distinct(),
            'memory': map(lambda memory: "{}GB".format(memory), subtype.objects.order_by('memory_size')
                          .values_list('memory_size', flat=True).distinct()),
            'hdmi ports': subtype.objects.order_by('hdmi_ports').values_list('hdmi_ports', flat=True).distinct(),
            'display ports': subtype.objects.order_by('dp_ports').values_list('dp_ports', flat=True).distinct()
        }

        return {**base_dimensions, **extra_dimensions}

    def get_filterable_dimension_name(self, ui_dimension_name):
        filterable_dimension_name = super(GPU, self).get_filterable_dimension_name(ui_dimension_name)

        if filterable_dimension_name is None:
            if ui_dimension_name == "chipset":
                filterable_dimension_name = "chipset"
            elif ui_dimension_name == "memory":
                filterable_dimension_name = "memory"
            elif ui_dimension_name == "hdmi ports":
                filterable_dimension_name = "hdmi_ports"
            else:
                filterable_dimension_name = "dp_ports"

        return filterable_dimension_name


class CPU(Component):
    cores = models.PositiveIntegerField(default=2)
    threads = models.PositiveIntegerField(default=4)
    socket = models.CharField(max_length=100)
    integrated_graphics = models.CharField(max_length=100, null=True)
    stock_freq = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    boost_freq = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    watts = models.PositiveIntegerField(default=0)
    l3_cache = models.CharField(max_length=20)

    def get_page_title(self):
        return "{} - {} {}Ghz {}-Core Processor".format(self.manufacturer, self.model_number,
                                                        self.stock_freq, self.cores)

    def get_tech_details(self):
        main_details = super(CPU, self).get_tech_details()
        extra_details = {
            "Socket Type": self.socket,
            "Stock Frequency": "{}Ghz".format(self.stock_freq),
            "Turbo Frequency": "{}Ghz".format(self.boost_freq),
            "Cores": self.cores,
            "Threads": self.threads,
            "L3 Cache": self.l3_cache,
            "Power Draw": "{} Watts".format(self.watts),
            "Integrated Graphics": self.integrated_graphics
        }

        return {**main_details, **extra_details}

    def get_filterable_dimensions(self, subtype):
        base_dimensions = super(CPU, self).get_filterable_dimensions(subtype)
        extra_dimensions = {
            'cores': subtype.objects.order_by('cores').values_list('cores', flat=True).distinct(),
            'socket type': subtype.objects.order_by('socket').values_list('socket', flat=True).distinct(),
            'integrated graphics': subtype.objects.order_by('integrated_graphics').values_list('integrated_graphics',
                                                                                               flat=True).distinct()
        }

        return {**base_dimensions, **extra_dimensions}

    def get_filterable_dimension_name(self, ui_dimension_name):
        filterable_dimension_name = super(CPU, self).get_filterable_dimension_name(ui_dimension_name)

        if filterable_dimension_name is None:
            if ui_dimension_name == "cores":
                filterable_dimension_name = "cores"
            elif ui_dimension_name == "socket type":
                filterable_dimension_name = "socket"
            else:
                filterable_dimension_name = "integrated_graphics"

        return filterable_dimension_name


class Monitor(Component):
    screen_size = models.PositiveIntegerField(default=10)
    resolution = models.CharField(max_length=100)
    aspect_ratio = models.CharField(max_length=100)
    response_time = models.PositiveIntegerField(default=10)
    refresh_rate = models.PositiveIntegerField(default=60)
    g_sync = models.CharField(max_length=100)
    dp_ports = models.IntegerField(default=0)
    hdmi_ports = models.IntegerField(default=0)
    panel_type = models.CharField(max_length=20)

    def get_page_title(self):
        resolution = "{}".format(self.resolution).replace(' ', "")
        return "{} - {} {}\" {} {}Hz Monitor".format(self.manufacturer, self.serial_number, self.screen_size,
                                                     resolution, self.refresh_rate)

    def get_tech_details(self):
        main_details = super(Monitor, self).get_tech_details()
        extra_details = {
            "Screen Size": "{}\"".format(self.screen_size),
            "Resolution": self.resolution,
            "Aspect Ratio": self.aspect_ratio,
            "Response Time": "{}ms".format(self.response_time),
            "Refresh Rate": "{}Hz".format(self.refresh_rate),
            "G-Sync": self.g_sync,
            "Panel Type": self.panel_type,
            "Displayport": self.dp_ports,
            "HDMI": self.hdmi_ports
        }

        return {**main_details, **extra_details}

    def get_filterable_dimensions(self, subtype):
        base_dimensions = super(Monitor, self).get_filterable_dimensions(subtype)
        extra_dimensions = {
            'recommended resolution': subtype.objects.order_by('resolution').values_list('resolution',
                                                                                         flat=True).distinct(),
            'response time': map(lambda time: "{}ms".format(time), subtype.objects.order_by('response_time').
                                 values_list('response_time', flat=True).distinct()),
            'refresh rate': map(lambda rate: "{}Hz".format(rate), subtype.objects.order_by('refresh_rate').
                                values_list('refresh_rate', flat=True).distinct()),
            'panel type': subtype.objects.order_by('panel_type').values_list('panel_type', flat=True).distinct()
        }

        return {**base_dimensions, **extra_dimensions}

    def get_filterable_dimension_name(self, ui_dimension_name):
        filterable_dimension_name = super(Monitor, self).get_filterable_dimension_name(ui_dimension_name)

        if filterable_dimension_name is None:
            if ui_dimension_name == "recommended resolution":
                filterable_dimension_name = "resolution"
            elif ui_dimension_name == "response time":
                filterable_dimension_name = "response_time"
            elif ui_dimension_name == "refresh rate":
                filterable_dimension_name = "refresh_rate"
            else:
                filterable_dimension_name = "panel_type"

        return filterable_dimension_name


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=1000)
    stars = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    time_added = models.DateTimeField(auto_now=True)
    time_edited = models.DateTimeField(auto_now=True)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.user, self.id)

    def save(self, *args, **kwargs):
        # must save first or we cannot find ourselves when updating component stats
        super(Review, self).save(*args, **kwargs)
        if self.component:
            self.component.update_ratings()

    def test(self):
        return self.objects.all()
