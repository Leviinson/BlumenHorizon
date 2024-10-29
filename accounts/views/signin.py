from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin

from core.services.mixins.views import CommonContextMixin
from ..forms import UserSignInForm


class UserLoginView(
    LoginView,
    CommonContextMixin,
    ContextMixin,
):
    extra_context = {"title": _("Вход")}
    template_name = "accounts/authorization/sign_in.html"
    redirect_authenticated_user = True
    authentication_form = UserSignInForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get('remember'):
            self.request.session.set_expiry(7 * 24 * 60 * 60)
        else:
            self.request.session.set_expiry(0)
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
