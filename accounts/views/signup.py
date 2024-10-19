from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic.base import ContextMixin

from core.services.mixins.views import CommonContextMixin

from ..forms.user_signup_form import UserSignUpForm


class UserSignUpView(CommonContextMixin, CreateView, ContextMixin):
    model = get_user_model()
    success_url = reverse_lazy("accounts:signin")
    form_class = UserSignUpForm
    template_name = "accounts/authorization/sign_up.html"
    extra_context = {"title": _("Регистрация")}

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        messages.success(
            self.request,
            _(
                f"Дорогой пользователь, зайдите на почту {email} и подтвердите активацию аккаунта."
            ),
        )
        return super().form_valid(form)
