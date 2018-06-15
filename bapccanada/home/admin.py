from django.contrib import admin
from products.models import GPU, Review
from build.models import Build

# Register your models here.
admin.site.register(GPU)
admin.site.register(Review)


class BuildAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)


admin.site.register(Build, BuildAdmin)
