from django.urls import path

from account import views


app_name = "account"
urlpatterns = [
    path("sign-in/", views.sign_in, name="sign-in"),
    path("log-in/", views.log_in, name="log-in"),
    path("log-out/", views.log_out, name="log-out"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("password/change", views.password_change, name="password-change"),
    path("profile-edit", views.profile_edit, name="profile-edit"),
]
