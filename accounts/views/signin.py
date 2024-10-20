from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin

from core.services.mixins.views import CommonContextMixin, NotAuthenticatedMixin


class UserLoginView(
    NotAuthenticatedMixin,
    CommonContextMixin,
    LoginView,
    ContextMixin,
):
    extra_context = {"title": _("Вход")}
    template_name = "accounts/authorization/sign_in.html"
