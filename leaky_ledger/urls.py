from django.urls import path

from .views.register import register
from .views.accounts import accounts
from .views.account import account
from .views.home import home

urlpatterns = [
    path("register", register, name="register"),
    path("accounts", accounts, name="accounts"),
    path("account/<int:account_id>/", account, name="account"),
    path("", home, name="home"),
]
