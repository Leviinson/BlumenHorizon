from dataclasses import asdict

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse_lazy

from .common_dataclasses.user import UserCredentials


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signup_url = reverse_lazy("accounts:signup")
        cls.signin_url = reverse_lazy("accounts:signin")
        cls.profile_url = reverse_lazy("accounts:me")

        User = get_user_model()
        cls.signin_data = UserCredentials(
            email="secret@gmail.com",
            phonenumber="+4915234815623",
            first_name="Vitalii",
            last_name="Melnykov",
            password=make_password("secret123321")
        )
        cls.user = User.objects.create(
            **asdict(cls.signin_data),
            is_active = True
        )
        cls.user.set_password("secret123321")
        super().setUpClass()
