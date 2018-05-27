from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import UserProfile, UserPreferences

admin.site.register(UserProfile)
admin.site.register(UserPreferences)



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
