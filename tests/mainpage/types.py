from typing import NamedTuple

from mainpage.models import MainPageModel, MainPageSeoBlock, MainPageSliderImages


class MainPageData(NamedTuple):
    mainpage: MainPageModel
    seoblock: MainPageSeoBlock
    slider_images: MainPageSliderImages
