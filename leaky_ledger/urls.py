from django.urls import path
from .views.register import register
from .views.home import home

urlpatterns = [
    path("register", register, name="register"),
    path("", home, name="home"),
]
