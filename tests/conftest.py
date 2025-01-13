import os

import pytest
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet

from catalogue.models import Bouquet

from .types import UrlsDataclass, UserCredentials, UserData


@pytest.fixture
def user_data(transactional_db) -> UserData:
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


@pytest.fixture
def bouquet_categories(db):
    pass


@pytest.fixture
def product_categories(db):
    pass


@pytest.fixture
def bouquet_subcategories(bouquet_categories):
    pass


@pytest.fixture
def product_subcategories(product_categories):
    pass


@pytest.fixture
def products(product_subcategories):
    pass


@pytest.fixture
def recommended_bouquets(db) -> QuerySet[Bouquet]:
    pass
