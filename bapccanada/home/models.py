from django.db import models
from django.db.models import Min, Max

from decimal import Decimal

from products.models import Component


class Price(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)
    shipping = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)
    store = models.CharField(max_length=100, default="")
    store_link = models.URLField()
    availability = models.CharField(max_length=100, default="In Stock")
    total_price = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.price) + Decimal(self.shipping)
        super(Price, self).save(*args, **kwargs)
        if self.component:
            self.component.update_cheapest_pricing()

    def __str__(self):
        return "{} : {}".format(self.id, self.store_link)

    @staticmethod
    def get_price_range(component_class_id):
        return {
            "min": Price.objects.filter(component__polymorphic_ctype_id=component_class_id).aggregate(Min('price'))["price__min"],
            "max": Price.objects.filter(component__polymorphic_ctype_id=component_class_id).aggregate(Max('price'))["price__max"]
        }


class Image(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True)
    image_link = models.URLField()

    def __str__(self):
        return "{} : {}".format(self.id, self.image_link)
