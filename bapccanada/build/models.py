from django.db import models
from django.template.defaultfilters import slugify

from functools import reduce
from decimal import Decimal

from products.models import GPU, CPU, Monitor
from user.models import UserProfile


class Build(models.Model):
    gpu = models.ForeignKey(GPU, null=True, on_delete=models.DO_NOTHING)
    cpu = models.ForeignKey(CPU, null=True, on_delete=models.DO_NOTHING)
    monitor = models.ForeignKey(Monitor, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    complete = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    total_price = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.total_price = self.get_total_price()
        super(Build, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.owner, self.name)

    def get_total_price(self):
        component_array = [self.gpu, self.cpu, self.monitor]
        component_array = map(lambda component: 0.0 if not component else (Decimal(component.cheapest_price) +
                                                                           Decimal(component.cheapest_price_shipping))
                              , component_array)

        return reduce(lambda total, current: total+current, component_array)

    def get_component_dict(self):
        return {
            "Video Card": {
                "object": self.gpu,
                "category_link": "products:gpu",
                "detail_link": "products:gpu_detail"
            },
            "Processor": {
                "object": self.cpu,
                "category_link": "products:cpu",
                "detail_link": "products:cpu_detail"
            },
            "Monitor": {
                "object": self.monitor,
                "category_link": "products:monitors",
                "detail_link": "products:monitor_detail"
            }
        }





