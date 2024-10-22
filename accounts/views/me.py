from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import FormMixin

from core.services.mixins.views import CommonContextMixin

from ..forms.user_form import UserForm


class UserprofileMenuMixin:
    tabs = {
        "profile": {
            "name": _("Профиль"),
            "url": reverse_lazy("accounts:me"),
            "disabled": False,
        },
        "settings": {
            "name": _("Настройки"),
            "url": "https://google.com",
            "disabled": True,
        },
        "orders": {
            "name": _("Заказы"),
            "url": "https://google.com",
            "disabled": True,
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tabs"] = self.tabs
        return context


class UserDetailView(
    LoginRequiredMixin,
    BaseDetailView,
    FormMixin,
    TemplateResponseMixin,
    UserprofileMenuMixin,
    CommonContextMixin,
    ContextMixin,
):
    model = get_user_model()
    template_name = "accounts/index.html"
    context_object_name = "user"
    form_class = UserForm
    extra_context = {"title": _("Личный кабинет")}

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        return super().get_initial()
