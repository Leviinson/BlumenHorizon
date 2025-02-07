from typing import Any


class OrderRepository:
    """
    Репозиторий для работы с заказами в контексте системы Stripe.

    Класс предоставляет методы для извлечения информации, связанной с заказами,
    из данных событий, получаемых от Stripe.
    """

    @classmethod
    def get_order_code(
        cls, event_dict: dict[str, Any | str | dict | list]
    ) -> str | None:
        """
        Извлекает код заказа из данных события Stripe.

        Метод анализирует структуру данных события, полученного от Stripe,
        и извлекает код заказа, хранящийся в метаданных объекта.

        Args:
            event_dict (dict[str, Any | str | dict | list]):
                Словарь, содержащий данные события Stripe.
                Ожидается, что структура словаря имеет следующую вложенность:
                - "data" -> "object" -> "metadata" -> "order_code".

        Returns:
            str: Код заказа, извлечённый из метаданных объекта Stripe.

        Raises:
            KeyError: Если один из ожидаемых ключей
            ("data", "object", "metadata") отсутствует в словаре.
        """
        return event_dict["data"]["object"]["metadata"].get("order_code")
