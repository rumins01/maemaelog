from django.urls import path
from tradestats import views

urlpatterns = [
    path("sidebar_right/", views.mystock_rank)
]
