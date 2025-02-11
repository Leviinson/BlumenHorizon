from typing import Any

from django.contrib.sites.models import Site
from django.core.cache import caches

from extended_contrib_models.models import ExtendedSite

cache = caches["default"]


def set_or_get_from_cache(key: str, timeout: int) -> Any:
    """
    Получает значение из кэша или устанавливает новое, если ключ отсутствует.

    Функция поддерживает обработку различных ключей, что позволяет гибко
    управлять данными в кэше. Если значение по заданному ключу `key` отсутствует,
    оно извлекается из соответствующего источника, сохраняется в кэше с указанным
    таймаутом `timeout` и возвращается. Если значение уже есть, оно просто извлекается
    из кэша.

    Args:
        key (str): Ключ для хранения или извлечения значения из кэша.
        timeout (int): Время хранения значения в кэше, в секундах.

    Returns:
        Any: Значение, связанное с ключом `key` (из кэша или вновь установленное).

    Raises:
        ValueError: Если обработка указанного ключа не поддерживается.
    """
    value_from_cache = cache.get(key)
    if value_from_cache is not None:
        return value_from_cache

    value = _get_value_for_key(key)
    cache.set(key, value, timeout)
    return value


def _get_value_for_key(key: str) -> Any:
    """
    Определяет источник данных для ключа и возвращает соответствующее значение.

    Args:
        key (str): Ключ для которого нужно получить значение.

    Returns:
        Any: Значение, соответствующее указанному ключу.

    Raises:
        ValueError: Если обработка указанного ключа не поддерживается.
    """
    match key:
        case "currency_symbol":
            return ExtendedSite.objects.only("currency_symbol").first().currency_symbol
        case "currency_code":
            return ExtendedSite.objects.only("currency_code").first().currency_code
        case "site_name":
            return Site.objects.only("name").first().name
        case "site_domain":
            return Site.objects.only("domain").first().domain
        case "site_email":
            return ExtendedSite.objects.only("email").first().email
        case "country_code":
            return (
                ExtendedSite.objects.only("country_iso_3166_1_alpha_2")
                .first()
                .country_iso_3166_1_alpha_2
            )
        case "country_name":
            return ExtendedSite.objects.only("country").first().country
        case "city_name":
            return ExtendedSite.objects.only("city").first().city
        case "socials":
            socials = (
                ExtendedSite.objects.prefetch_related("socials").first().socials.all()
            )
            return [social.to_dict() for social in socials]
        case "header_alert_message":
            return (
                ExtendedSite.objects.only("header_alert_message")
                .first()
                .header_alert_message
            )
        case _:
            raise ValueError(f"Unsupported cache key: {key}")
