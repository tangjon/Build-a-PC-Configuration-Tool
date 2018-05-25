from django.db import models
from django.template.defaultfilters import slugify

from polymorphic.models import PolymorphicModel

from home.models import Price, Image
from user.models import UserProfile


class Component(PolymorphicModel):
    manufacturer = models.CharField(max_length=30)
    model_number = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30, blank=True)

    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    images = models.ManyToManyField(Image)
    prices = models.ManyToManyField(Price)
    cheapest_price = models.DecimalField(default=0.0, max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.manufacturer, self.model_number)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.model_number)
        super(Component, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    stars = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    time_added = models.DateTimeField(auto_now=True)
    time_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.id)


class GPU(Component):
    clock_rate = models.DecimalField(default=0.0, max_digits=3, decimal_places=2, blank=True, null=True)
    chipset = models.CharField(max_length=100)
    clock_rate_oc = models.DecimalField(default=0.0, max_digits=3, decimal_places=2, blank=True, null=True)
    memory_size = models.PositiveIntegerField(default=10)
    hdmi_ports = models.PositiveIntegerField(default=0)
    dp_ports = models.PositiveIntegerField(default=0)


class CPU(Component):
    cores = models.PositiveIntegerField(default=2)
    threads = models.PositiveIntegerField(default=4)
    socket = models.CharField(max_length=100)
    integrated_graphics = models.CharField(max_length=100, null=True)
    stock_freq = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    boost_freq = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    watts = models.CharField(max_length=50)
    l3_cache = models.CharField(max_length=20)


class Monitor(Component):
    screen_size = models.PositiveIntegerField(default=10)
    resolution = models.CharField(max_length=100)
    aspect_ratio = models.CharField(max_length=100)
    response_time = models.CharField(max_length=100)
    refresh_rate = models.CharField(max_length=100)
    g_sync = models.CharField(max_length=100)
    dp_ports = models.IntegerField(default=0)
    hdmi_ports = models.IntegerField(default=0)
    panel_type = models.CharField(max_length=20)
