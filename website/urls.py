from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("our-work/", views.our_work, name="our_work"),
    path("find-us/", views.find_us, name="find_us"),
]
