from django.contrib.sessions.backends.base import SessionBase

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
    products_cart = ProductCart(session=session, session_key="products_cart")
    bouquets_cart = BouquetCart(session=session, session_key="bouquets_cart")
    return products_cart, bouquets_cart
