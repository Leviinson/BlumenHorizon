from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path

from .views.me import UserDetailView
from .views.signup import UserSignUpView

app_name = "accounts"

urlpatterns = [
    path("", login_required(UserDetailView.as_view()), name="me"),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path(
        "signin/",
        LoginView.as_view(
            template_name="accounts/authorization/sign_in.html",
        ),
        name="signin",
    ),
]
