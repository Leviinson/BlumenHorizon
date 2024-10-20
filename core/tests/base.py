from dataclasses import asdict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.sites.models import Site

from .common_dataclasses.user import UserCredentials


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signup_url = reverse_lazy("accounts:signup")
        cls.signin_url = reverse_lazy("accounts:signin")
        cls.profile_url = reverse_lazy("accounts:me")
        site = Site.objects.get(id=1)
        site.name = settings.SITE_NAME
        site.domain = settings.SITE_DOMAIN
        site.save(update_fields=["name", "domain",])

        User = get_user_model()
        cls.test_user_password = "secret123321"
        cls.test_user_data = UserCredentials(
            email="secret@gmail.com",
            phonenumber="+4915234815623",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        cls.user = User(
            **asdict(cls.test_user_data),
            is_active = True
        )
        cls.user.set_password(cls.test_user_password)
        cls.user.save()
        super().setUpClass()
