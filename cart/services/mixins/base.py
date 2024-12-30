from django.contrib.sessions.backends.base import SessionBase
from django.db.models import OuterRef, Subquery
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

from catalogue.models import Bouquet, BouquetImage, Product, ProductImage


class CartMixin:
    image_model: ProductImage | BouquetImage

    def __init__(
        self,
        with_images: bool = False,
        session: SessionBase = None,
        session_key: str = None,
        *args,
        **kwargs,
    ):
        self.with_images = with_images
        return super().__init__(session, session_key, *args, **kwargs)

    def get_quantity(self, product: Product | Bouquet):
        """
        Возвращает кол-во продукта в корзине.

        :param product: Выбранный продукт для получения значения.
        """
        if product in self.products:
            return self._items_dict[product.pk].quantity

    def get_subtotal(self, product: Product | Bouquet):
        """
        Возвращает стоимость продукта в корзине (учитывая его кол-во).

        :param product: Выбранный продукт для получения значения.
        """
        if product in self.products:
            return self._items_dict[product.pk].subtotal

    def filter_products(
        self, queryset: QuerySet[Product | Bouquet]
    ) -> QuerySet[Product | Bouquet]:
        """
        Подготавливает дополнительную информацию о товарах,
        которая будет использована при отображении корзины
        товаров на странице корзины пользователя.

        :param queryset: QuerySet модели, переданный средствами \
        django-carton. Просто QuerySet указанный для модели продукта \
        корзины конкректного типа (ProductCart или BouquetCart), \
        без каких либо вмешательств.
        """
        from django.utils.translation import get_language

        language = get_language()

        base_queryset = super().filter_products(queryset)
        optimized_queryset: QuerySet = self.get_optimized_queryset(base_queryset)
        if self.with_images:
            optimized_queryset = self.attach_first_image_of_each_item(
                optimized_queryset, language
            )

        queryset_result = self.fetch_required_fields_from_optimized_queryset(
            optimized_queryset
        )
        return queryset_result

    def get_optimized_queryset(
        self, base_queryset: QuerySet[Product | Bouquet]
    ) -> QuerySet[Product | Bouquet]:
        """
        Подхватывает связанные модели, поля которых будут
        использованы в self.fetch_required_fields_from_optimized_queryset.

        Параметры:
        :param base_queryset: Отфильтрованный queryset силами django-carton.
        """
        optimized_queryset = base_queryset.select_related(
            "subcategory", "subcategory__category"
        )
        return optimized_queryset

    def attach_first_image_of_each_item(
        self, optimized_queryset: QuerySet[Product | Bouquet], language: str
    ) -> QuerySet[Product | Bouquet]:
        """
        Этот метод нужен чтобы достать только первое изображение
        продукта который будет в корзине пользователя, так как
        на странице корзины продуктов показывается только первое
        фото. Данный метод сокращает нагрузку, так как не
        захватывает лишние фотографии.

        Параметры:
        :param optimized_queryset: Отфильтрованный или подхвативший связанные \
        модели queryset через select/prefetch_related.
        :param language: Выбранный язык для image alternate среди зарегистрированных.
        """
        first_image_subquery = self.get_subquery_of_first_image(
            self.image_model
        )
        optimized_queryset = optimized_queryset.annotate(
            first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
            first_image_alt=Subquery(
                first_image_subquery.values(f"image_alt_{language}")[:1]
            ),
        )
        return optimized_queryset

    def get_subquery_of_first_image(
        self,
        image_model: ProductImage | BouquetImage,
    ) -> BaseManager[Product | Bouquet]:
        """
        Этот метод используется для конструкции запроса ORM,
        который захватит только первое фото товара.

        Параметры:
        :param image_model: Модель, которая отвечает за сбережение \
        путей фотографий конкретной модели товара (ProductImage или BouquetImage)
        """
        first_image_subquery = image_model.objects.filter(
            item = OuterRef("pk")
        ).order_by("id")[:1]
        return first_image_subquery

    def fetch_required_fields_from_optimized_queryset(
        self, optimized_queryset: QuerySet[Product | Bouquet]
    ) -> QuerySet[Product | Bouquet]:
        """
        Этот метод используется чтобы достать нужные поля
        из моделей после выполнения фильтрации и аннотирования,
        как того требует Django, и естественно для получения полей
        которые будут использоваться, без захвата лишних полей
        чтобы снизить нагрузку.

        Параметры:
        :param optimized_queryset: Готовый к отбору полей queryset, \
        после фильтрации и аннотирования.
        """
        queryset_result = optimized_queryset.only(
            "name",
            "slug",
            "price",
            "discount",
            "discount_expiration_datetime",
            "is_active",
            "subcategory__is_active",
            "subcategory__category__is_active",
            "subcategory__slug",
            "subcategory__category__slug",
        )
        return queryset_result
