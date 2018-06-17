from django.db import models

# Create your models here.
from linkshortener.utils import generate_link, create_shortcode


class BapcUrl(models.Model):
    url = models.URLField()
    shortcode = models.CharField(max_length=6, unique=True, blank=True)

    def __str__(self):
        return str(self.url)

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(instance=BapcUrl)
        super(BapcUrl, self).save(*args, **kwargs)
