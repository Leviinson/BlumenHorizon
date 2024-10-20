from dataclasses import asdict
from core.tests.base import BaseTestCase
from core.tests.common_dataclasses.user import UserSignUpCredentials


class UserAuthenticationTest(BaseTestCase):

    def test_user_authentication(self):
        response = self.client.post(self.signin_url, asdict(self.signin_data))
        self.assertTrue(response.context["user"].is_authenticated, "User is not authenticated")
        self.assertRedirects(response, self.profile_url)
