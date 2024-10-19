from django.test import TestCase
from django.urls import reverse_lazy


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signup_url = reverse_lazy("accounts:signup")
        cls.signin_url = reverse_lazy("accounts:signin")
        super().setUpClass()
