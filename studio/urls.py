from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("style/<slug:slug>/", views.style_detail, name="style_detail"),
]