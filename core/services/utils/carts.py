from typing import Any

from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.models import Session
from django.utils import timezone

from cart.cart import BouquetCart, ProductCart


def get_carts(session: SessionBase) -> tuple[ProductCart, BouquetCart]:
    """
    Сессия пользователя хранит в себе две корзины: корзина стандартных продуктов
    и корзина букетов.

    Поскольку это разные сущности то их корзины так-же разделены.
    При расшифровке тела сессии из базы данных - эти корзины доступны под
    ключами «products_cart» и «bouquets_cart».

    :param session: сессия из запроса пользователя (self.request.session)
    """
    products_cart = ProductCart(session=session, session_key=ProductCart.session_key)
    bouquets_cart = BouquetCart(session=session, session_key=BouquetCart.session_key)
    return products_cart, bouquets_cart


def clear_user_cart(session_key: str) -> None:
    """
    Очищает корзину пользователя по ключу сессии.

    Параметры:
    - session_key (str): Ключ сессии, связанной с корзиной.

    Исключения:
    - Session.DoesNotExist: Если сессия не найдена или истекла.
    """
    try:
        session = Session.objects.filter(expire_date__gt=timezone.now()).get(
            session_key=session_key
        )
        session_dict = session.get_decoded()
        products_cart: dict[str, dict | Any] = session_dict.get("products_cart")
        bouquets_cart: dict[str, dict | Any] = session_dict.get("bouquets_cart")
        if products_cart:
            products_cart.clear()
        if bouquets_cart:
            bouquets_cart.clear()

        session_store_class = session.get_session_store_class()
        session.session_data = session_store_class().encode(session_dict)
        session.save(update_fields=["session_data"])
    except Session.DoesNotExist:
        pass
