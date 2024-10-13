import phonenumbers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.base_models import TimeStampModelMixin


class UserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, *args, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, *args, **kwargs)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(email, password, **extra_fields)


class User(TimeStampModelMixin, AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(verbose_name=_("Электронная почта"), unique=True)
    phone_number = models.CharField(
        max_length=15, verbose_name=_("Номер телефона"), null=True, blank=True
    )
    first_name = models.CharField(_("Имя"), max_length=150, null=True, blank=True)
    last_name = models.CharField(_("Фамилия"), max_length=150, null=True, blank=True)
    is_staff = models.BooleanField(
        "Администратор?",
        default=False,
        help_text=_("Определяет может ли пользователь попасть в админ-панель"),
        editable=False,
    )
    is_active = models.BooleanField(
        "Активный?",
        default=False,
        help_text=_(
            f"Определяет может ли пользователь авторизоваться."
            f" Выберите это вместо удаления аккаунта!!!"
        ),
    )
    is_superuser = models.BooleanField(
        "Суперпользователь?",
        default=False,
        editable=False,
        help_text=f"Определяет имеет ли пользователь доступ ко всему "
        f"без предварительного разрешения.",
    )
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def clean(self):
        super().clean()

    def clean_phonenumber(self):
        if self.phone_number:
            try:
                parsed_number = phonenumbers.parse(self.phone_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError(_("Некорректный номер телефона."))
            except phonenumbers.NumberParseException:
                raise ValidationError(_("Некорректный формат номера телефона."))

    def get_short_name(self):
        """Return the short name for the user."""
        return self.last_name
