from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from cart.cart import BouquetCart, ProductCart
from catalogue.models import (
    Bouquet,
    BouquetImage,
    BouquetsListPageModel,
    Product,
    ProductImage,
    ProductsListPageModel,
)
from core.services.utils.first_image_attaching import annotate_first_image_and_alt


class ListViewMixin:
    """
    Миксин для отображения и обработки списков товаров или букетов.

    Атрибуты класса:
    - `allow_empty` (bool): Разрешает отображение пустого списка (по умолчанию True).
    - `paginate_by` (int): Количество элементов на странице (по умолчанию 8).
    - `image_model` (type): Модель для работы с изображениями товаров или букетов.
    - `page_model` (type): Модель для работы с данными страницы (мета-теги, настройки).

    Константы:
    - `SORT_OPTIONS` (list): Опции для сортировки выборки, такие как:
        - Цена по убыванию.
        - Цена по возрастанию.
        - По алфавиту.
        - Со скидкой.
    """

    allow_empty = False
    paginate_by = 8
    image_model: type[ProductImage] | type[BouquetImage]
    page_model: type[ProductsListPageModel] | type[BouquetsListPageModel]

    SORT_OPTIONS = [
        {"name": _("Цена по убыванию"), "value": "pd"},
        {"name": _("Цена по возрастанию"), "value": "pi"},
        {"name": _("По алфавиту"), "value": "alph"},
        {"name": _("Со скидкой"), "value": "disc"},
    ]

    def get_queryset(self) -> QuerySet[Bouquet | Product]:
        """
        Получает queryset объектов с учётом сортировки и фильтрации.

        Этот метод определяет текущий язык с помощью `get_language`, извлекает выбранную
        опцию сортировки из GET-параметров, получает базовый queryset и применяет сортировку
        и фильтрацию. Также добавляется первое изображение к каждому объекту.

        :returns: Отсортированный и обработанный queryset.
        """
        from django.utils.translation import get_language

        language = get_language()
        selected_option = self.get_selected_option_for_sorting(self.request.GET)
        queryset = self.get_queryset_for_sorting()
        sorted_queryset = self.sort_queryset_by_selected_option(
            queryset,
            selected_option,
            self.image_model,
            language,
        )
        return sorted_queryset

    @staticmethod
    def get_selected_option_for_sorting(get_params: dict[str, str]):
        """
        Извлекает выбранную пользователем опцию сортировки из GET-параметров.

        :param get_params: Словарь GET-параметров текущего запроса.
        :type get_params: dict[str, str]

        :returns: Код выбранной опции сортировки (например, "pd", "pi", "alph", "disc").
            По умолчанию возвращается "pd" (цена по убыванию).
        """
        return get_params.get("sort", "pd")

    def get_queryset_for_sorting(self) -> QuerySet[Product | Bouquet]:
        """
        Получает базовый queryset для дальнейшей обработки.

        :returns: Исходный queryset.
        :rtype: QuerySet[Product | Bouquet]
        """
        return super().get_queryset()

    def sort_queryset_by_selected_option(
        self,
        queryset: QuerySet[Product | Bouquet],
        selected_option: str,
        image_model: ProductImage | BouquetImage,
        language: str,
    ) -> QuerySet[Bouquet | Product]:
        """
        Применяет сортировку, фильтрацию и добавляет изображение к каждому объекту в queryset.

        Этот метод:
        - Сортирует queryset в зависимости от выбранной опции.
        - Фильтрует queryset, включая только активные элементы.
        - Добавляет первое изображение (если оно есть) к каждому объекту в queryset.

        :param queryset: Исходный queryset для обработки.
        :type queryset: QuerySet[Product | Bouquet]

        :param selected_option: Опция сортировки, выбранная пользователем.
        :type selected_option: str

        :param image_model: Модель, используемая для получения изображений.
        :type image_model: ProductImage | BouquetImage

        :param language: Код текущего языка.
        :type language: str

        :returns: Обработанный и отсортированный queryset.
        :rtype: QuerySet[Bouquet | Product]
        """
        sorted_queryset = self.order_queryset_by_selected_option(
            queryset,
            selected_option,
        )
        queryset_with_active_items = self.filter_queryset_by_active_items(
            sorted_queryset,
        )
        result = self.attach_first_image_to_queryset_items(
            queryset_with_active_items,
            image_model,
            language,
        )
        return result

    @staticmethod
    def order_queryset_by_selected_option(
        queryset: QuerySet[Bouquet | Product], selected_option: str
    ) -> QuerySet[Bouquet | Product]:
        """
        Сортирует queryset в зависимости от выбранной опции сортировки.

        Поддерживаемые опции:
        - "pd": по убыванию цены.
        - "pi": по возрастанию цены.
        - "alph": по алфавиту.
        - "disc": по убыванию скидки.

        :param queryset: queryset для сортировки.
        :type queryset: QuerySet[Bouquet | Product]

        :param selected_option: Опция сортировки, выбранная пользователем.
        :type selected_option: str

        :returns: Отсортированный queryset.
        :rtype: QuerySet[Bouquet | Product]
        """
        match selected_option:
            case "pd":
                queryset = queryset.order_by("-price")
            case "pi":
                queryset = queryset.order_by("price")
            case "alph":
                queryset = queryset.order_by("name")
            case "disc":
                queryset = queryset.order_by("-discount")
        return queryset

    @staticmethod
    def filter_queryset_by_active_items(
        queryset: QuerySet[Bouquet | Product],
    ) -> QuerySet[Bouquet | Product]:
        """
        Фильтрует queryset, оставляя только активные элементы.

        Этот метод гарантирует, что элементы, их подкатегории и категории будут помечены как активные.

        :param queryset: queryset для фильтрации.
        :type queryset: QuerySet[Bouquet | Product]

        :returns: Отфильтрованный queryset, содержащий только активные элементы.
        :rtype: QuerySet[Bouquet | Product]
        """
        queryset = queryset.filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        )
        return queryset

    def attach_first_image_to_queryset_items(
        self,
        queryset: QuerySet[Bouquet | Product],
        image_model: ProductImage | BouquetImage,
        language: str,
    ) -> QuerySet[Bouquet | Product]:
        """
        Добавляет первое изображение (URI и alt текст) к каждому элементу в queryset.

        Этот метод использует подзапрос для получения первого изображения каждого объекта
        и добавляет URI изображения и локализованный alt текст в queryset.

        :param queryset: queryset для аннотирования.
        :type queryset: QuerySet[Bouquet | Product]

        :param image_model: Модель, используемая для получения изображений.
        :type image_model: ProductImage | BouquetImage

        :param language: Код текущего языка.
        :type language: str

        :returns: Обновлённый queryset с добавленными изображениями.
        :rtype: QuerySet[Bouquet | Product]
        """
        return annotate_first_image_and_alt(queryset, image_model, language)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sort_options"] = self.SORT_OPTIONS
        page: ProductsListPageModel | BouquetsListPageModel = (
            self.page_model.objects.first()
        )
        context["meta_tags"] = page.meta_tags
        return context


class ProductListViewMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["cart"] = ProductCart(
            session=self.request.session, session_key=ProductCart.session_key
        )
        context["add_to_cart_uri"] = reverse_lazy("cart:product-add")
        context["remove_from_cart_uri"] = reverse_lazy("cart:product-remove")
        return context


class BouquetListViewMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["cart"] = BouquetCart(
            session=self.request.session, session_key=BouquetCart.session_key
        )
        context["add_to_cart_uri"] = reverse_lazy("cart:bouquet-add")
        context["remove_from_cart_uri"] = reverse_lazy("cart:bouquet-remove")
        return context
