from django.urls import path
from django.contrib.auth.views import LoginView

from .views.login import login_view
from .views.register import register
from .views.accounts import accounts
from .views.internal_transfer import internal_transfer
from .views.external_transfer import external_transfer
from .views.account import account
from .views.user_lookup import user_lookup
from .views.home import home

urlpatterns = [
    path("accounts/login", login_view, name="login"),
    path("register", register, name="register"),
    path("accounts", accounts, name="accounts"),
    path("transfer/internal", internal_transfer, name="internal_transfer"),
    path("transfer/external", external_transfer, name="external_transfer"),
    path("account/<int:account_id>/", account, name="account"),
    path("users/lookup/", user_lookup, name="user_lookup"),
    path("", home, name="home"),
]
