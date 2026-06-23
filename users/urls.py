from django.urls import path, include
from . import views
from django.shortcuts import redirect
from .views import set_password, cancel_password_setup



urlpatterns = [
    path("accounts/signup/", lambda request: redirect("account_login")),
    path("accounts/3rdparty/login/cancelled/", lambda request: redirect("account_login")),
    path('accounts/', include('allauth.urls')),

    path("account/set-password/", set_password, name="set_password"),
    path("account/cancel-password-setup/", cancel_password_setup, name="cancel_password_setup"),
]   