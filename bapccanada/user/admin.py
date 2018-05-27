from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import UserProfile, PrivacySettings, ClickSettings, EmailSettings


# ===================
# CUSTOM ADMIN
# ===================

class ClickOptionsInline(admin.StackedInline):
    model = PrivacySettings
    verbose_name_plural = 'Click Options'
    fk_name = 'profile'


class PrivacyOptionsInline(admin.StackedInline):
    model = ClickSettings
    verbose_name_plural = 'Privacy Options'
    fk_name = 'profile'


class EmailOptionsInline(admin.StackedInline):
    model = EmailSettings
    verbose_name_plural = 'Email Options'
    fk_name = 'profile'


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (ClickOptionsInline, PrivacyOptionsInline,EmailOptionsInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserProfileAdmin, self).get_inline_instances(request, obj)


admin.site.register(UserProfile, UserProfileAdmin)

# ===================
# STANDARD ADMIN
# ===================


# COMBINE EVERYTHING USERPROFILE RELATED

# class UserPreferencesInline(admin.StackedInline):
#     model = UserPreferences
#     verbose_name_plural = 'Preferences'
#     fk_name = 'profile'
#
#
# class UserProfileAdmin(admin.ModelAdmin):
#     inlines = (UserPreferencesInline,)
#
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(UserProfileAdmin, self).get_inline_instances(request, obj)
#
#
# admin.site.register(UserProfile, UserProfileAdmin)

# COMBINE USER AND USERPROFILE

# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'
#
#
# class CustomUserAdmin(UserAdmin):
#     inlines = (UserProfileInline,)
#
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
