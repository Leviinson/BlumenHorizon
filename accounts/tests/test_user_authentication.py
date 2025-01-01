from typing import TypedDict

import pytest
from django.test import Client
from pytest_django.asserts import assertRedirects

from accounts.models import User
from core.tests.types.urls import UrlsDataclass
from core.tests.types.user import UserPassword


class TestUserAuthentication:
    """
    Тесты для проверки аутентификации пользователей через электронную почту и номер телефона.

    Этот класс включает в себя тесты для аутентификации пользователя, использующего email
    или номер телефона в качестве имени пользователя. Он также проверяет правильность
    перенаправления и успешной аутентификации через POST-запрос.
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
        site,
        urls: UrlsDataclass,
        db,
    ):
        """
        Тестирование аутентификации пользователя с использованием email.

        В этом тесте проверяется возможность аутентификации пользователя,
        используя его email в качестве имени пользователя.

        Аргументы:
            user_data (tuple[User, UserPassword]): Кортеж, содержащий объект пользователя \
                                                    и его пароль.
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
        site,
        user_data: tuple[User, UserPassword],
        urls: UrlsDataclass,
        db,
    ):
        """
        Тестирование аутентификации пользователя с использованием номера телефона.

        В этом тесте проверяется возможность аутентификации пользователя,
        используя его номер телефона в качестве имени пользователя.

        Аргументы:
            user_data (tuple[User, UserPassword]): Кортеж, содержащий объект пользователя \
                                                    и его пароль.
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

        Эта функция отправляет POST-запрос с данными аутентификации и проверяет,
        что пользователь был успешно аутентифицирован и перенаправлен на страницу профиля.

        Аргументы:
            signin_data (UserAuthenticationData): Данные для аутентификации, содержащие имя пользователя \
                                                  и пароль.
        """
        response = client.post(signin_url, signin_data)
        assertRedirects(response, UrlsDataclass.profile)
        assert response.wsgi_request.user.is_authenticated, "User is not authenticated"
