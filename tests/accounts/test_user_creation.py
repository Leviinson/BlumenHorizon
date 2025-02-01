from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertFormError

from accounts.models import User

from ..types import UrlsDataclass, UserSignUpCredentials


class TestUserCreation:

    def test_user_creation(self, client: Client, urls: UrlsDataclass, site, db):
        """
        Тестирование создания нового пользователя.

        Этот тест проверяет, что пользователь может успешно зарегистрироваться,
        при этом данные пользователя сохраняются в базе данных, а также что он
        получает письмо для активации аккаунта, которое активирует его.

        Аргументы:
            client: Клиент Django для отправки HTTP-запросов.
            urls (UrlsDataclass): Содержит все URL для тестирования регистрации.
            site: Модель сайта, которая будет использоваться в тестируемом коде. \
                Необходимо наличие её записи и модели с расширенными данными, чтобы \
                тестируемый endpoint работал.
            db: Доступ к базе данных для выполнения операций в тестах.
        """
        signup_data = self._get_signup_data()
        response = self._submit_signup_form(client, urls, signup_data)
        self._verify_user_in_db(signup_data)
        user = self._get_user_from_db(signup_data["email"])
        self._verify_user_data(user, signup_data)
        self._verify_user_inactive(user)
        self._activate_user_via_email(response, user)
        self._verify_user_active(user)

    def _get_signup_data(self) -> UserSignUpCredentials:
        """
        Подготовка данных для регистрации пользователя.

        Эта функция возвращает данные, которые будут использованы для регистрации
        нового пользователя, включая email, пароль и другие обязательные поля.

        Возвращает:
            dict: Данные для регистрации пользователя.
        """
        return UserSignUpCredentials(
            email="melnykov.vitalii197@gmail.com",
            password1="fhjeuio**^321",
            password2="fhjeuio**^321",
            first_name="Vitalii",
            last_name="Melnykov",
            phonenumber_0="DE",
            phonenumber_1="15234815621",
        )

    def _submit_signup_form(
        self, client: Client, urls: UrlsDataclass, signup_data: dict
    ) -> HttpResponse:
        """
        Отправка формы регистрации.

        Эта функция выполняет POST-запрос с данными регистрации и возвращает ответ,
        чтобы проверить дальнейшие шаги, такие как перенаправление.

        Аргументы:
            client (Client): Клиент Django для отправки HTTP-запросов.
            urls (UrlsDataclass): Содержит URL-адрес для отправки данных.
            signup_data (dict): Данные, которые будут отправлены в форме регистрации.

        Возвращает:
            response: Ответ сервера после отправки формы регистрации.
        """
        return client.post(urls.signup, signup_data)

    def _verify_user_in_db(self, signup_data: dict) -> None:
        """
        Проверка, что пользователь был успешно создан в базе данных.

        Эта функция выполняет запрос в базу данных, чтобы проверить, был ли создан
        пользователь с указанным email.

        Аргументы:
            signup_data (dict): Данные регистрации пользователя, используемые для проверки.
        """
        user_filtered = get_user_model().objects.filter(email=signup_data["email"])
        assert user_filtered.exists(), "User record wasn't created."

    def _get_user_from_db(self, email: str) -> User:
        """
        Получение пользователя из базы данных по email.

        Эта функция возвращает пользователя из базы данных по указанному email.

        Аргументы:
            email (str): Email пользователя для поиска.

        Возвращает:
            user: Объект пользователя из базы данных.
        """
        return get_user_model().objects.get(email=email)

    def _verify_user_data(self, user: User, signup_data: UserSignUpCredentials) -> None:
        """
        Проверка данных пользователя в базе данных.

        Эта функция проверяет, что данные пользователя, сохраненные в базе данных,
        соответствуют ожидаемым данным, отправленным на регистрацию.

        Аргументы:
            user: Объект пользователя из базы данных.
            signup_data (dict): Ожидаемые данные пользователя.
        """
        assert user.email == signup_data["email"]
        assert user.phonenumber == "+49" + signup_data["phonenumber_1"]
        assert user.first_name == signup_data["first_name"]
        assert user.last_name == signup_data["last_name"]
        assert user.check_password(signup_data["password1"])

    def _verify_user_inactive(self, user: User) -> None:
        """
        Проверка, что пользователь не активирован после регистрации.

        Эта функция проверяет, что пользователь не активирован сразу после регистрации.

        Аргументы:
            user: Объект пользователя из базы данных.
        """
        assert not user.is_active

    def _activate_user_via_email(
        self, response: HttpResponse, user: User
    ) -> HttpResponse:
        """
        Активация пользователя через email ссылку.

        Эта функция генерирует ссылку для активации пользователя через email и выполняет
        запрос для активации пользователя.

        Аргументы:
            response: Ответ на запрос регистрации, используется для получения URL для активации.
            user: Объект пользователя, которого нужно активировать.
        """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirm_email_url = response.wsgi_request.build_absolute_uri(
            reverse_lazy("accounts:activate", kwargs={"uidb64": uid, "token": token})
        )
        response = response.client.get(confirm_email_url)

    def _verify_user_active(self, user: User) -> None:
        """
        Проверка, что пользователь активирован после подтверждения по email.

        Эта функция проверяет, что пользователь был активирован после перехода по ссылке
        для активации из email.

        Аргументы:
            user: Объект пользователя из базы данных.
        """
        user.refresh_from_db()
        assert user.is_active, "User wasn't activated after email confirmation by link"


class TestDuplicatedUserCreation:
    def test_user_creation_with_duplicated_phonenumber(
        self, client: Client, urls: UrlsDataclass, site: Site, db
    ):
        """
        Тестирование создания пользователя с дублирующимся номером телефона.

        Этот тест проверяет, что при попытке зарегистрировать нового пользователя
        с уже существующим номером телефона возвращается ошибка.

        Аргументы:
            client: Клиент Django для отправки HTTP-запросов.
            urls (UrlsDataclass): Содержит все URL для тестирования регистрации.
            site: Модель сайта, которая будет использоваться в тестируемом коде. \
                  Необходимо наличие её записи и модели с расширенными данными, чтобы \
                  тестируемый endpoint работал.
            db: Доступ к базе данных для выполнения операций в тестах.
        """
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
        site: Site,
    ):
        """
        Тестирование создания пользователя с дублирующимся email.

        Этот тест проверяет, что при попытке зарегистрировать нового пользователя
        с уже существующим email адресом возвращается ошибка.

        Аргументы:
            client: Клиент Django для отправки HTTP-запросов.
            urls (UrlsDataclass): Содержит все URL для тестирования регистрации.
            site (Site): Модель сайта, которая будет использоваться в тестируемом коде. \
                  Необходимо наличие её записи и модели с расширенными данными, чтобы \
                  тестируемый endpoint работал.
        """
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
        assertFormError(
            response.context["form"],
            "email",
            "Пользователь с этой электронной почтой уже существует.",
        )
