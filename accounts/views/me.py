from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.services.mixins.views import CommonContextMixin


class UserDetailView(LoginRequiredMixin, CommonContextMixin, BaseDetailView, TemplateView):
    model = get_user_model()
    template_name = "accounts/index.html"
    context_object_name = "user"
    extra_context = {"title": _("Личный кабинет")}

    def get_object(self, queryset=None):
        return self.request.user
