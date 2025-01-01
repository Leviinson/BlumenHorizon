from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertFormError, assertRedirects

from accounts.models import User
from core.tests.types.urls import UrlsDataclass
from core.tests.types.user import UserSignUpCredentials


class TestUserCreation:

    def test_user_creation(
        self, client: Client, urls: UrlsDataclass, site, transactional_db
    ):
        signup_data = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_0="DE",
            phonenumber_1="15234815621",
        )
        response = client.post(urls.signup, signup_data)
        assertRedirects(response, urls.signin)

        user_filtered = get_user_model().objects.filter(email=signup_data["email"])
        assert user_filtered.exists(), "User record wasn't created."

        user: User = user_filtered.first()
        assert user.email == signup_data["email"]
        assert user.phonenumber == "+49" + signup_data["phonenumber_1"]
        assert user.first_name == signup_data["first_name"]
        assert user.last_name == signup_data["last_name"]
        assert user.check_password(signup_data["password1"])
        assert not user.is_active

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirm_email_url = response.wsgi_request.build_absolute_uri(
            reverse_lazy("accounts:activate", kwargs={"uidb64": uid, "token": token})
        )
        client.get(confirm_email_url)
        user = get_user_model().objects.get(pk=user.pk)
        assert user.is_active, "User wasn't activated after email confirmation by link"

    def test_user_creation_with_duplicated_phonenumber(
        self, client: Client, urls: UrlsDataclass, site, transactional_db
    ):
        signup_data_1 = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_0="DE",
            phonenumber_1="15234815621",
        )
        client.post(urls.signup, signup_data_1)

        signup_data_2 = UserSignUpCredentials(
            email="another-email@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_0="DE",
            phonenumber_1="15234815621",
        )
        response = client.post(urls.signup, signup_data_2)

        assert response.status_code == 200
        assertFormError(
            response.context["form"],
            "phonenumber",
            "Пользователь с этим номером телефона уже существует.",
        )

    def test_user_creation_with_duplicated_email(
        self,
        client: Client,
        urls: UrlsDataclass,
        site,
        db,
    ):
        signup_data_1 = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_0="DE",
            phonenumber_1="15234815621",
        )
        client.post(urls.signup, signup_data_1)

        signup_data_2 = UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_0="DE",
            phonenumber_1="15234815622",
        )
        response = client.post(urls.signup, signup_data_2)

        assert response.status_code == 200
        print(response.context["form"].errors)
        assertFormError(
            response.context["form"],
            "email",
            "Пользователь с этой электронной почтой уже существует.",
        )
