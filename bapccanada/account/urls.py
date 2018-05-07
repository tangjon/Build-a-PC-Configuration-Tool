from django.urls import re_path, path

from . import views

# lets follow reddit url format
# i.e /user/MrPotato
# .. /user/MrPotato/profile
# .. /user/MrPotato/preferences
app_name = 'account'
urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('preferences/', views.view_preferences, name="view_preferences"),
    path('comments/', views.view_comments, name="view_comments"),
    path('builds/', views.view_builds, name="view_builds"),
    path('notifications/', views.view_notifications, name="view_notifications"),
    path('security/', views.view_security, name="view_security")

]
