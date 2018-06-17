from django.db import models


# Create your models here.
class BapcUrl(models.Model):
    url = models.URLField()
