from dataclasses import asdict, dataclass

from core.tests.base import BaseTestCase


class UserAuthenticationTest(BaseTestCase):
    @dataclass
    class TestUserAuthenticationData:
        username: str
        password: str

    def test_user_authentication_with_email(self):
        self.__test_user_authenticatinon(
            self.TestUserAuthenticationData(
                username=self.test_user_data.email,
                password=self.test_user_password,
            )
        )

    def test_user_authentication_with_phonenumber(self):
        self.__test_user_authenticatinon(
            self.TestUserAuthenticationData(
                username=self.test_user_data.phonenumber,
                password=self.test_user_password,
            )
        )

    def __test_user_authenticatinon(self, signin_data: dict[str, str]):
        response = self.client.post(self.signin_url, asdict(signin_data))
        self.assertRedirects(response, self.profile_url)
        self.assertTrue(
            response.wsgi_request.user.is_authenticated,
            "User is not authenticated",
        )
