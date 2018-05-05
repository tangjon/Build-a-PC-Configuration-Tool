from django.db import models

import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


class Component(models.Model):
    manufacturer = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30, blank=True)
    cheapest_store = models.CharField(max_length=30, blank=True)
    store_link = models.URLField(max_length=300, blank=True)

    price = models.IntegerField(default=0)
    release_year = models.IntegerField(default=2000)
    shipping_cost = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GPU(Component):
    model_number = models.CharField(max_length=30)

    clock_rate = models.IntegerField(default=1000)
    clock_rate_oc = models.IntegerField(blank=True)
    cuda_cores = models.IntegerField(default=2)
    hdmi_ports = models.IntegerField(default=0)
    vga_ports = models.IntegerField(default=0)
    dp_ports = models.IntegerField(default=0)

    overclocked = models.BooleanField(default=False)

    def __str__(self):
        return "{} : {}".format(self.manufacturer, self.model_number)

    class Meta:
        unique_together = ("manufacturer", "model_number")


class Build(models.Model):
    gpu = models.ManyToManyField(GPU)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)


class Review(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    build = models.ForeignKey(Build, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=1000)
    stars = models.IntegerField(default=0)
    time_added = models.DateTimeField(auto_now=True)
    time_edited = models.DateTimeField(auto_now=True)
