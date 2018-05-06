from django.contrib import admin
from home.models import GPU, Review, Build, UserProfile

# Register your models here.
admin.site.register(GPU)
admin.site.register(Review)
admin.site.register(Build)
admin.site.register(UserProfile)
