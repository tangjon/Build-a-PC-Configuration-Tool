from django.contrib.auth.decorators import login_required
from django.urls import re_path, path

from user.views import *
from . import views

# lets follow reddit url format
# i.e /user/MrPotato
# .. /user/MrPotato/profile
# .. /user/MrPotato/preferences
app_name = 'user'
urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('preferences/', PreferencesView.as_view(), name="preferences"),
    path('comments/', ReviewView.as_view(), name="comments"),
    path('comments/delete/', review_delete, name="review_delete"),
    path('comments/update/', review_update, name="review_update"),
    path('builds/', BuildsView.as_view(), name="builds"),
    path('builds/<int:pk>', BuildsView.as_view(), name="builds"),
    path('builds/edit', BuildsView.as_view(), name="builds_edit"),
    path('security/', SecurityView.as_view(), name="security"),
    path('saved/', SavedView.as_view(), name="saved")
]
