from django.urls import path

from .views.register import register
from .views.accounts import accounts
from .views.account import account
from .views.user_lookup import user_lookup
from .views.home import home

urlpatterns = [
    path("register", register, name="register"),
    path("accounts", accounts, name="accounts"),
    path("account/<int:account_id>/", account, name="account"),
    path("users/lookup/", user_lookup, name="user_lookup"),
    path("", home, name="home"),
]
