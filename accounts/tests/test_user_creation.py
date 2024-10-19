from dataclasses import asdict, dataclass

from django.contrib.auth import get_user_model

from core.tests.base import BaseTestCase


@dataclass
class UserCredentials:
    email: str
    password1: str
    password2: str
    first_name: str
    last_name: str
    phonenumber_0: str = "DE"
    phonenumber_1: str = "15234815621"


class UserCreationTest(BaseTestCase):

    def create_user(self, signup_data: UserCredentials):
        return self.client.post(self.signup_url, asdict(signup_data))

    def assert_form_error(self, form, field, message):
        self.assertFalse(form.is_valid(), f"Form should not be valid for {field}")
        self.assertIn(field, form.errors)
        self.assertEqual(form.errors[field][0], message)

    def test_getting_reverse_url(self):
        str(self.signin_url)

    def test_user_creation(self):
        signup_data = UserCredentials(
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

    def test_user_creation_with_duplicated_phone_number(self):
        signup_data_1 = UserCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        self.create_user(signup_data_1)

        signup_data_2 = UserCredentials(
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
        signup_data_1 = UserCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
        )
        self.create_user(signup_data_1)

        signup_data_2 = UserCredentials(
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
