import pytest

from mainpage.models import MainPageModel, MainPageSeoBlock, MainPageSliderImages

from .types import MainPageData


@pytest.fixture
def mainpage(db) -> MainPageData:
    mainpage = MainPageModel.objects.create(
        meta_tags="<title> | BlumenHorizon</title>",
        json_ld_description="Blumen Horizon интернет-магазин цветов и подарков в Берлине",
        description="Описание странички в самом низу.",
    )

    mainpage_seo_block = MainPageSeoBlock.objects.create(
        image="tests/default_image_for_tests.jpg", image_alt="Описание сео-блока."
    )
    mainpage_slider_images = MainPageSliderImages.objects.create(
        image="tests/default_image_for_tests.jpg",
        image_alt="Описание изображения для слайдера на главной странице.",
        is_active=True,
    )
    return mainpage, mainpage_seo_block, mainpage_slider_images

