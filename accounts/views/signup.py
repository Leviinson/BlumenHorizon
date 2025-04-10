from typing import Type

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic.base import ContextMixin

from core.services.mixins import CommonContextMixin
from core.services.repositories import SiteRepository

from ..forms import UserSignUpForm
from ..services.mixins import NotAuthenticatedMixin


class UserSignUpView(
    NotAuthenticatedMixin,
    CommonContextMixin,
    CreateView,
    ContextMixin,
):
    success_url = reverse_lazy("accounts:signin")
    form_class = UserSignUpForm
    template_name = "accounts/authorization/sign_up.html"
    extra_context = {"title": _("Регистрация")}

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            self.send_email_confirmation_link(
                self.request, first_name, last_name, user, to_email=email
            )
        return HttpResponseRedirect(self.success_url)

    def send_email_confirmation_link(
        self,
        request: HttpRequest,
        first_name: str,
        last_name: str,
        user: Type[AbstractBaseUser],
        to_email: str,
    ):
        site_name = SiteRepository.get_name()

        mail_subject = _("{site_name} | Подтвердите Ваш Email").format(
            site_name=site_name
        )

        message = render_to_string(
            "accounts/email_confirmation/email_body.html",
            {
                "first_name": first_name,
                "last_name": last_name,
                "domain": SiteRepository.get_domain(),
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            },
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        if email.send():
            messages.success(
                request,
                _(
                    f"Дорогой пользователь, зайдите на почту {to_email} и подтвердите активацию аккаунта."
                ),
            )
        else:
            messages.error(
                request,
                _(
                    f"Дорогой пользователь, неудалось отправить письмо с просьбой о подтверждении почты. Проверьте правильно ли она написана: {email}"
                ),
            )


def decode_uid(uidb64: str) -> str:
    """
    Декодирует UID из base64 в строку.

    :param uidb64: Закодированный в base64 идентификатор пользователя.
    :return: UID в виде строки.
    """
    return force_str(urlsafe_base64_decode(uidb64))


def get_user_by_uid(uid: str):
    """
    Получает пользователя по UID.

    :param uid: Идентификатор пользователя.
    :return: Объект пользователя или None, если не найден.
    """
    User = get_user_model()
    try:
        return User.objects.only("pk").get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def activate_user(user) -> None:
    """
    Активирует пользователя, установив флаг is_active в True.

    :param user: Объект пользователя.
    """
    user.is_active = True
    user.save(update_fields=["is_active"])


def activate_user_account(
    request: HttpRequest, uidb64: str, token: str
) -> HttpResponse:
    """
    Активация учётной записи пользователя по ссылке, полученной на почту.

    Декодирует UID, получает пользователя, проверяет токен и активирует аккаунт.
    Отображает соответствующее сообщение и перенаправляет пользователя.

    :param request: HTTP-запрос.
    :param uidb64: Закодированный UID пользователя.
    :param token: Токен подтверждения.
    :return: HTTP-ответ с перенаправлением.
    """
    uid = decode_uid(uidb64)
    user = get_user_by_uid(uid)

    if user is not None and default_token_generator.check_token(user, token):
        activate_user(user)
        messages.success(
            request,
            _("Ваша почта успешно подтверждена, теперь Вы можете пойти в аккаунт."),
        )
        return redirect("accounts:signin")

    messages.error(
        request,
        _("Ссылка для подтверждения почты истекла или неверна."),
    )
    return redirect("accounts:signup")
