from dataclasses import dataclass, field
from typing import TypedDict
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import FormMixin

from core.services.mixins import CommonContextMixin

from ..forms.user_form import UserForm


class MenuTab(TypedDict):
    name: str
    url: str
    is_disabled: bool


class UserprofileMenuTabs(TypedDict):
    profile: MenuTab
    settings: MenuTab
    orders: MenuTab


class UserprofileMenuMixin:
    tabs = UserprofileMenuTabs(
        profile=MenuTab(
            name=_("Профиль"),
            url=reverse_lazy("accounts:me"),
            is_disabled=False,
        ),
        settings=MenuTab(
            name=_("Настройки"),
            is_disabled=True,
        ),
        orders=MenuTab(
            name=_("Заказы"),
            is_disabled=True,
        ),
    )

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
