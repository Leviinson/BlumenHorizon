from dataclasses import asdict

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.tests.common_dataclasses.user import UserSignUpCredentials


class UserCreationTest(TestCase):

    def setUp(self):
        self.signup_url = reverse_lazy("accounts:signup")
        self.signin_url = reverse_lazy("accounts:signin")
        return super().setUp()

    def create_user(self, signup_data: UserSignUpCredentials):
        return self.client.post(self.signup_url, asdict(signup_data))

    def assert_form_error(self, form, field, message):
        self.assertFalse(form.is_valid(), f"Form should not be valid for {field}")
        self.assertIn(field, form.errors)
        self.assertEqual(form.errors[field][0], message)

    def test_getting_reverse_url(self):
        str(self.signin_url)

    def test_user_creation(self):
        signup_data = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        response = self.create_user(signup_data)
        self.assertRedirects(response, self.signin_url)

        user_filtered = get_user_model().objects.filter(email=signup_data.email)
        self.assertTrue(user_filtered.exists(), "User record wasn't created.")

        user = user_filtered.first()
        self.assertEqual(user.email, signup_data.email)
        self.assertEqual(user.phonenumber, "+49" + signup_data.phonenumber_1)
        self.assertEqual(user.first_name, signup_data.first_name)
        self.assertEqual(user.last_name, signup_data.last_name)
        self.assertTrue(user.check_password(signup_data.password1))
        self.assertFalse(user.is_active)

        protocol = ("https://" if response.wsgi_request.is_secure() else "http://",)
        domain = get_current_site(response.wsgi_request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirm_email_url = (
            protocol[0]
            + domain
            + reverse_lazy("accounts:activate", kwargs={"uidb64": uid, "token": token})
        )
        self.client.get(confirm_email_url)
        user = get_user_model().objects.get(pk=user.pk)
        self.assertTrue(
            user.is_active,
            "User wasn't activated after email confirmation by link",
        )

    def test_user_creation_with_duplicated_phonenumber(self):
        signup_data_1 = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        self.create_user(signup_data_1)

        signup_data_2 = UserSignUpCredentials(
            email="secret197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        response = self.create_user(signup_data_2)

        self.assertEqual(response.status_code, 200)
        self.assert_form_error(
            response.context["form"],
            "phonenumber",
            "Пользователь с этим номером телефона уже существует.",
        )

    def test_user_creation_with_duplicated_email(self):
        signup_data_1 = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        self.create_user(signup_data_1)

        signup_data_2 = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_1="15234815622",
        )
        response = self.create_user(signup_data_2)

        self.assertEqual(response.status_code, 200)
        self.assert_form_error(
            response.context["form"],
            "email",
            "Пользователь с этой электронной почтой уже существует.",
        )
