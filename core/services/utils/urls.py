import logging

from django.conf import settings

from core.services.repositories import SiteRepository

from ..types import AbsoluteUri, RelativeUri

logger = logging.getLogger("django.request")


def build_absolute_uri(
    relative_uri: RelativeUri, is_media: bool = False, is_static: bool = False
) -> AbsoluteUri:
    domain = SiteRepository.get_domain()
    protocol = "https" if settings.SECURE_SSL_REDIRECT else "http"
    match is_media, is_static:
        case True, False:
            pass
        case False, True:
            media_url = settings.MEDIA_URL
            return f"{protocol}://{domain}{media_url}{relative_uri}"
        case False, False:
            return f"{protocol}://{domain}{relative_uri}"
        case _:
            logger.error(
                f"В утилите {build_absolute_uri.__module__}.{build_absolute_uri.__name__} "
                f"неправильно переданы аргументы is_media ({is_media}) "
                f"и is_static ({is_static})."
            )
            raise ValueError("Ошибка значения аргументов is_media & is_static")
