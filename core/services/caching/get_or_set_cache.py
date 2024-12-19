from typing import Any

from django.contrib.sites.models import Site
from django.core.cache import cache

from extended_contrib_models.models import ExtendedSite


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
        case "tax_percent":
            return ExtendedSite.objects.only("tax_percent").first().tax_percent
        case "currency_symbol":
            return ExtendedSite.objects.only("currency_symbol").first().currency_symbol
        case "currency_code":
            return ExtendedSite.objects.only("currency_code").first().currency_code
        case "site_name":
            return Site.objects.only("name").first().name
        case "domain":
            return Site.objects.only("domain").first().domain
        case _:
            raise ValueError(f"Unsupported cache key: {key}")
