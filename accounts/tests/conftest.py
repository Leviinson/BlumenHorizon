import os

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import pytest
from accounts.models import User
from core.tests.types.urls import UrlsDataclass
from core.tests.types.user import UserCredentials, UserPassword


@pytest.fixture
def user_data(db) -> tuple[User, UserPassword]:
    User = get_user_model()
    test_user_data = UserCredentials(
        email="secret@gmail.com",
        phonenumber="+4915234815623",
        first_name="Vitalii",
        last_name="Melnykov",
    )
    password = "secret123321"
    user = User(**test_user_data, is_active=True)
    user.set_password(password)
    user.save()
    return user, password


@pytest.fixture
def site(db) -> Site:
    site = Site.objects.get(id=1)
    site.name = os.getenv("SITE_NAME")
    site.domain = os.getenv("SITE_DOMAIN")

    site.save(
        update_fields=[
            "name",
            "domain",
        ]
    )
    site = Site.objects.get(id=1)
    return site


@pytest.fixture(scope="session")
def urls() -> UrlsDataclass:
    return UrlsDataclass()
