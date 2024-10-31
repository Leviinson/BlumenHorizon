from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserSignInForm(AuthenticationForm):
    remember = forms.BooleanField(required=False, initial=False)

    error_messages = {
        "invalid_login": _(
            "Пожалуйста, введите корректную электронную почту и пароль. Помните, что "
            "оба поля чувствительны к регистру"
        ),
        "inactive": _(
            "Почта не подтверждена. Мы отправили письмо на Вашу почту, "
            'проверьте папку "Входящие"/"Спам".'
        ),
    }
