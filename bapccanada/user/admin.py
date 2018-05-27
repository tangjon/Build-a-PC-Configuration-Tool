from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import UserProfile, UserSettings


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    verbose_name_plural = 'Settings'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, UserSettingsInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
