from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms.user_signup_form import UserSignUpForm


class UserSignUpView(CreateView):
    model = get_user_model()
    success_url = reverse_lazy("accounts:me")
    form_class = UserSignUpForm
    template_name = "accounts/authorization/sign_up.html"
