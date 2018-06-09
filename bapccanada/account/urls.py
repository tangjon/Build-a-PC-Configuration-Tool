from django.urls import re_path, path, include, reverse, reverse_lazy
from django.contrib.auth import views
from account.views import UserCreate, LoginView, LogoutView

# lets follow reddit url format
# i.e /user/MrPotato
# .. /user/MrPotato/profile
# .. /user/MrPotato/preferences

app_name = 'account'
urlpatterns = [
    # re_path(r'^login/$', SignIn.as_view(), name="sign_in"),
    # re_path(r'^logout/$', Logout.as_view(), name="logout"),
    path('signup/', UserCreate.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    # PASSWORD CHANGE
    path('password_change/', views.PasswordChangeView.as_view(template_name="password_change_form.html",
                                                              success_url=reverse_lazy('account:password_change_done')),
         name='password_change'),
    path('password_change/done/',
         views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
         name='password_change_done'),
    # PASSWORD RESET
    path('password_reset/', views.PasswordResetView.as_view(template_name="password_reset_form.html",
                                                            success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",
                                                                           success_url=reverse_lazy(
                                                                               'account:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete')
]
