from django.urls import re_path, path

from . import views

# lets follow reddit url format
# i.e /user/MrPotato
# .. /user/MrPotato/profile
# .. /user/MrPotato/preferences
app_name = 'account'
urlpatterns = [
    path('', views.view_profile, name='profile'),
    path('preferences/', views.view_preferences, name="preferences"),
    path('comments/', views.view_comments, name="comments"),
    path('builds/', views.view_builds, name="builds"),
    path('notifications/', views.view_notifications, name="notifications"),
    path('security/', views.view_security, name="security")

]
