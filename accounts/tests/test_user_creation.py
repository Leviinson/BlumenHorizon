from dataclasses import asdict, dataclass
from pprint import pprint

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import NoReverseMatch, reverse_lazy


class UserCreationTest(TestCase):

    @dataclass
    class UserCredentials:
        email: str = "melnykov.vitalii197@gmail.com"
        password1: str = "fhjeuio**^321"
        password2: str = "fhjeuio**^321"
        first_name: str = "Vitalii"
        last_name: str = "Melnykov"

    def setUp(self):
        self.signup_url = reverse_lazy("accounts:signup")
        self.signin_url = reverse_lazy("accounts:signin")
        self.signup_data = self.UserCredentials()
        return super().setUp()
    
    def test_getting_reverse_url(self):
        str(self.signin_url)

    def test_user_creation(self):

        response = self.client.post(self.signup_url, asdict(self.signup_data))
        if response.status_code == 200 and response.content["form"].errors:
            self.fail(
                f"Form errors: {response.context["form"].errors}.\nUser wasn't created."
            )
        self.assertRedirects(response, self.signin_url)

        user_filtered = get_user_model().objects.filter(email=self.signup_data.email)
        self.assertTrue(
            user_filtered.exists(),
            f"The controller of user creation returned 201 code"
            f" but record in DB wasn't created.",
        )
        user = user_filtered.first()
        self.assertEqual(
            user.email,
            self.signup_data.email,
            "Username from request and in DB is different",
        )
        self.assertEqual(
            user.first_name,
            self.signup_data.first_name,
            "User first name from request and in DB is different",
        )
        self.assertEqual(
            user.last_name,
            self.signup_data.last_name,
            "User last name from request and in DB is different",
        )
        self.assertTrue(
            user.check_password(self.signup_data.password1),
            "Password from request and in DB is different",
        )
        self.assertTrue(
            user.is_authenticated,
            "User wasn't authenticated",
        )
        self.assertFalse(
            user.is_anonymous,
            "User was authenticated and is anonymous at the same time",
        )
        self.assertFalse(
            user.is_active, "User is active but email wasn't confirmed yet"
        )
        self.assertFalse(user.is_staff, "User was created as staff")
        self.assertFalse(user.is_superuser, "User was created as is_superuser")
