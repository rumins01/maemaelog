from django.urls import path

from account import views


app_name = "account"
urlpatterns = [
    path("sign-in/", views.sign_in, name="sign-ip"),
    path("log-in/", views.log_in, name="log-in"),
    path("log-out/", views.log_out, name="log-out"),
]
