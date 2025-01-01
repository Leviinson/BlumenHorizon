from typing import TypedDict

from django.contrib.sites.models import Site
from django.test import Client
from pytest_django.asserts import assertRedirects

from accounts.models import User
from core.tests.types.urls import UrlsDataclass
from core.tests.types.user import UserPassword


class TestUserAuthentication:
    """
    Тесты для проверки аутентификации пользователей через электронную почту и номер телефона.

    Этот класс включает в себя тесты для проверки аутентификации пользователя,
    используя его email или номер телефона в качестве имени пользователя. Тесты также проверяют
    правильность перенаправления после успешной аутентификации и проверяют, что пользователь
    был аутентифицирован через POST-запрос.
    """

    class UserAuthenticationData(TypedDict):
        """
        Класс для хранения данных аутентификации пользователя.

        Атрибуты:
            username (str): Имя пользователя (email или номер телефона).
            password (str): Пароль пользователя.
        """

        username: str
        password: str

    def test_user_authentication_with_email(
        self,
        client: Client,
        user_data: tuple[User, UserPassword],
        site: Site,
        urls: UrlsDataclass,
        db,
    ):
        """
        Тестирование аутентификации пользователя с использованием email.

        Этот тест проверяет возможность аутентификации пользователя, используя его email как имя пользователя.
        При успешной аутентификации пользователь должен быть перенаправлен на страницу профиля.

        Аргументы:
            user_data (tuple[User, UserPassword]): Кортеж, содержащий объект пользователя и его пароль.
            site: Модель сайта, которая будет использоваться в тестируемом коде. \
            Необходимо наличие её записи и модели с расширенными данными чтобы
            тестируемый endpoint работал.
            urls (UrlsDataclass): Содержит все URL для тестирования аутентификации.
            db: Доступ к базе данных для выполнения операций в тестах.
        """
        user, password = user_data
        self.__test_user_authenticatinon(
            client,
            self.UserAuthenticationData(
                username=user.email,
                password=password,
            ),
            urls.signin,
        )

    def test_user_authentication_with_phonenumber(
        self,
        client: Client,
        site: Site,
        user_data: tuple[User, UserPassword],
        urls: UrlsDataclass,
        db,
    ):
        """
        Тестирование аутентификации пользователя с использованием номера телефона.

        Этот тест проверяет возможность аутентификации пользователя,
        используя его номер телефона как имя пользователя.
        При успешной аутентификации пользователь должен быть
        перенаправлен на страницу профиля.

        Аргументы:
            user_data (tuple[User, UserPassword]): Кортеж, содержащий объект пользователя и его пароль.
            site: Модель сайта, которая будет использоваться в тестируемом коде. \
            Необходимо наличие её записи и модели с расширенными данными чтобы
            тестируемый endpoint работал.
            urls (UrlsDataclass): Содержит все URL для тестирования аутентификации.
            db: Доступ к базе данных для выполнения операций в тестах.
        """
        user, password = user_data
        self.__test_user_authenticatinon(
            client,
            self.UserAuthenticationData(
                username=user.phonenumber,
                password=password,
            ),
            urls.signin,
        )

    def __test_user_authenticatinon(
        self, client: Client, signin_data: UserAuthenticationData, signin_url: str
    ):
        """
        Вспомогательная функция для выполнения аутентификации пользователя.

        Эта функция отправляет POST-запрос с данными аутентификации и проверяет, что пользователь был успешно аутентифицирован
        и перенаправлен на страницу профиля. Она также проверяет, что пользователь действительно аутентифицирован.

        Аргументы:
            signin_data (UserAuthenticationData): Данные для аутентификации, содержащие имя пользователя и пароль.
            signin_url (str): URL для выполнения POST-запроса для аутентификации пользователя.
        """
        response = client.post(signin_url, signin_data)
        assertRedirects(response, UrlsDataclass.profile)
        assert response.wsgi_request.user.is_authenticated, "User is not authenticated"
