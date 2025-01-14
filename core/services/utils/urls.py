import logging

from django.conf import settings

from core.services.repositories import SiteRepository

from ..types import AbsoluteUrl, RelativeUrl

logger = logging.getLogger("django.request")


def build_absolute_url(
    relative_url: RelativeUrl, is_static: bool = False
) -> AbsoluteUrl:
    """
    Генерирует абсолютный URL на основе переданных аргументов.

    :param relative_url: Относительный URL, который будет дополнен до абсолютного.
    :param is_static: Флаг, указывающий на необходимость использования STATIC_URL.
    :return: Абсолютный URL.
    """

    domain = SiteRepository.get_domain()
    protocol = "https" if settings.SECURE_SSL_REDIRECT else "http"

    if is_static:
        return f"{protocol}://{domain}{settings.STATIC_URL}{relative_url}"

    return f"{protocol}://{domain}{relative_url}"
