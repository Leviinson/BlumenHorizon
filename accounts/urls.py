from django.contrib.auth.decorators import login_required
from django.urls import path

from .views.me import UserDetailView
from .views.signin import UserLoginView
from .views.signup import UserSignUpView, activate_user_account

app_name = "accounts"

urlpatterns = [
    path("", login_required(UserDetailView.as_view()), name="me"),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("signin/", UserLoginView.as_view(), name="signin"),
    path("activate/<uidb64>/<token>/", activate_user_account, name="activate"),
]
