from django.db import models
from django.db.models import Min
from django.db.models.signals import m2m_changed
from django.template.defaultfilters import slugify

from polymorphic.models import PolymorphicModel
import decimal

from home.models import Price, Image
from user.models import UserProfile


class Component(PolymorphicModel):
    manufacturer = models.CharField(max_length=30)
    model_number = models.CharField(max_length=30, blank=True)
    serial_number = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=100, default="")

    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    images = models.ManyToManyField(Image)
    prices = models.ManyToManyField(Price)
    cheapest_price = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)

    average_rating = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    num_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.manufacturer, self.model_number)

    def save(self, *args, **kwargs):
        self.display_name = "{} {}".format(self.manufacturer, self.serial_number)
        self.slug = slugify(self.model_number)
        super(Component, self).save(*args, **kwargs)

    def update_ratings(self, new_rating):
        previous_score = decimal.Decimal(self.average_rating) * self.num_ratings
        self.num_ratings += 1
        new_score = (previous_score + new_rating.stars) / self.num_ratings
        self.average_rating = new_score
        self.save()


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
    watts = models.PositiveIntegerField(default=0)
    l3_cache = models.CharField(max_length=20)


class Monitor(Component):
    screen_size = models.PositiveIntegerField(default=10)
    resolution = models.CharField(max_length=100)
    aspect_ratio = models.CharField(max_length=100)
    response_time = models.PositiveIntegerField(default=10)
    refresh_rate = models.CharField(max_length=100)
    g_sync = models.CharField(max_length=100)
    dp_ports = models.IntegerField(default=0)
    hdmi_ports = models.IntegerField(default=0)
    panel_type = models.CharField(max_length=20)


def prices_changed(sender, **kwargs):
    if kwargs["action"] == "post_add" and kwargs["model"] == Price:
        current_component = kwargs["instance"]
        current_min_price = current_component.prices.all().aggregate(Min('price'))["price__min"]
        if current_component.cheapest_price == 0.0 or current_min_price < current_component.cheapest_price:
            current_component.cheapest_price = current_min_price
            current_component.save()


# many to many handler to update lowest price
m2m_changed.connect(prices_changed, sender=Component.prices.through)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=1000)
    stars = models.DecimalField(default=0.0, max_digits=2, decimal_places=1, blank=True, null=True)
    time_added = models.DateTimeField(auto_now=True)
    time_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.id)

    def save(self, *args, **kwargs):
        if self.component:
            self.component.update_ratings(new_rating=self)
            self.component.save()
        super(Review, self).save(*args, **kwargs)