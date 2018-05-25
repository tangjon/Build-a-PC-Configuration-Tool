from django.db import models


class Price(models.Model):
    price = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)
    shipping = models.DecimalField(default=0.0, max_digits=19, decimal_places=2, blank=True, null=True)
    store = models.CharField(max_length=100)
    store_link = models.URLField()

    def __str__(self):
        return "{} : {}".format(self.id, self.store_link)


class Image(models.Model):
    image_link = models.URLField()

    def __str__(self):
        return "{} : {}".format(self.id, self.image_link)
