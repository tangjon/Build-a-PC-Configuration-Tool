from django.db import models


class Price(models.Model):
    price = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    store = models.CharField(max_length=100)
    store_link = models.URLField()

    def __str__(self):
        return "{} : {}".format(self.id, self.store_link)


class Image(models.Model):
    image_link = models.URLField()

    def __str__(self):
        return "{} : {}".format(self.id, self.image_link)
