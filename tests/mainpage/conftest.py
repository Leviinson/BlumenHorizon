from typing import TypedDict

import pytest
from django.contrib.sites.models import Site

from extended_contrib_models.models import ExtendedSite, Social
from mainpage.models import MainPageModel, MainPageSeoBlock, MainPageSliderImages

from .types import MainPageData


@pytest.fixture
def create_mainpage(db) -> MainPageModel:
    """Создает основную модель главной страницы."""
    return MainPageModel.objects.create(
        meta_tags="<title> | BlumenHorizon</title>",
        json_ld_description="Blumen Horizon интернет-магазин цветов и подарков в Берлине",
        description="Описание странички в самом низу.",
    )


@pytest.fixture
def create_mainpage_seo_block(db) -> MainPageSeoBlock:
    """Создает SEO-блок для главной страницы."""
    return MainPageSeoBlock.objects.create(
        image="tests/default_image_for_tests.jpg", image_alt="Описание сео-блока."
    )


@pytest.fixture
def create_mainpage_slider_image(db) -> MainPageSliderImages:
    """Создает изображение для слайдера на главной странице."""
    return MainPageSliderImages.objects.create(
        image="tests/default_image_for_tests.jpg",
        image_alt="Описание изображения для слайдера на главной странице.",
        is_active=True,
    )


class ExpectedSocial(TypedDict):
    absolute_url: str
    outline_hex_code: str
    background_hex_code: str
    icon_hex_code: str
    bootstrap_icon: str
    extended_site: ExtendedSite


EXPECTED_SOCIALS = [
    ExpectedSocial(
        absolute_url="https://t.me/levinsxn/",
        outline_hex_code="#000000",
        background_hex_code="#111111",
        icon_hex_code="#222222",
        bootstrap_icon="telegram",
    ),
    ExpectedSocial(
        absolute_url="https://instagram.com/",
        outline_hex_code="#333333",
        background_hex_code="#444444",
        icon_hex_code="#555555",
        bootstrap_icon="instagram",
    ),
    ExpectedSocial(
        absolute_url="https://facebook.com/",
        outline_hex_code="#666666",
        background_hex_code="#777777",
        icon_hex_code="#888888",
        bootstrap_icon="facebook",
    ),
]


@pytest.fixture
def create_socials(db, site: Site) -> list[Social]:
    """Создает объекты социальных сетей для связанного сайта."""
    extended_site = ExtendedSite.objects.get(site=site)
    socials_models_list = []
    for social in EXPECTED_SOCIALS:
        social["extended_site"] = extended_site
        socials_models_list.append(Social(**social))
    return Social.objects.bulk_create(socials_models_list)


@pytest.fixture
def mainpage(
    create_mainpage,
    create_mainpage_seo_block,
    create_mainpage_slider_image,
    create_socials,
) -> MainPageData:
    """Объединяет все данные главной страницы в одну фикстуру."""
    return (
        create_mainpage,
        create_mainpage_seo_block,
        create_mainpage_slider_image,
        create_socials,
    )
