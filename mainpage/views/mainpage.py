from typing import Any, Callable

import requests
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from catalogue.models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    Product,
    ProductCategory,
    ProductImage,
)
from core.services.dataclasses.related_model import RelatedModel
from core.services.mixins import CommonContextMixin
from core.services.mixins.canonicals import CanonicalLinksMixin
from core.services.mixins.common_context_mixin import CanonicalsContextMixin
from core.services.types import Limit, OrderedModelField
from core.services.utils.carts import get_carts
from core.services.utils.recommended_items import get_recommended_items_with_first_image

from ..forms import IndividualOrderForm
from ..models import MainPageModel, MainPageSeoBlock, MainPageSliderImages
from .types import Categories, RecommendedItems


class MainPageView(
    CommonContextMixin,
    CanonicalLinksMixin,
    CanonicalsContextMixin,
    TemplateView,
):
    template_name = "mainpage/index.html"
    http_method_names = ["get"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return self.build_context(base_context=context)

    def build_context(self, base_context: dict[str, Any]) -> dict[str, Any]:
        """
        Расширяет базовый контекст контроллера дополнительными ключами для генерации
        контента главной страницы.

        :param base_context: Контекст контроллера, созданный суперклассом.
        """
        base_context["slider_images"] = MainPageSliderImages.objects.filter(
            is_active=True
        ).all()

        base_context["recommended_bouquets"], base_context["recommended_products"] = (
            self.get_recommended_items_tuple(
                processor=get_recommended_items_with_first_image,
            )
        )
        base_context["products_cart"], base_context["bouquets_cart"] = get_carts(
            self.request.session
        )
        base_context["products_categories"], base_context["bouquets_categories"] = (
            self.get_categories_tuple()
        )

        # Форма определяется отдельно, так как отправка происходит
        # посредством AJAX-запроса
        base_context["individual_order_form"] = IndividualOrderForm()
        base_context["seo_block"] = MainPageSeoBlock.objects.first()

        page_model = MainPageModel.objects.first()
        base_context["description"] = page_model.description
        base_context["meta_tags"] = page_model.meta_tags
        base_context["json_ld_description"] = page_model.json_ld_description
        base_context["elfsight_widget"] = self.get_elfsight_widget_js()
        return base_context

    @staticmethod
    def get_categories_tuple() -> Categories:
        """
        Возвращает категории букетов и стандартных продуктов из Базы Данных.

        Используется для секции с перечислением всех категорий под H1 тегом
        главной страницы. [пример](https://imgur.com/a/NRX4tKB)
        """
        products_categories = (
            ProductCategory.objects.filter(is_active=True)
            .prefetch_related("subcategories")
            .only(
                "name",
                "slug",
                "code_value",
                "subcategories__code_value",
                "subcategories__slug",
                "subcategories__name",
            )
        )
        bouquets_categories = (
            BouquetCategory.objects.filter(is_active=True)
            .prefetch_related("subcategories")
            .only(
                "name",
                "slug",
                "code_value",
                "subcategories__code_value",
                "subcategories__slug",
                "subcategories__name",
            )
        )
        return products_categories, bouquets_categories

    @staticmethod
    def get_recommended_items_tuple(
        processor: Callable[
            [
                Product | Bouquet,
                ProductImage | BouquetImage,
                list[RelatedModel],
                list[OrderedModelField],
                Limit,
            ],
            RecommendedItems,
        ],
    ) -> RecommendedItems:
        """
        Возвращает рекомендованные букеты и продукты, используя переданную функцию процессора.

        Данная функция используется для получения рекомендованных товаров (букетов и продуктов)
        для различных слайдеров и секций на страницах (например, «Рекомендованные букеты к покупке» и
        «Рекомендуемые подарки к букетам» на главной странице и в корзине пользователя).

        Вызов processor с передачей параметров для моделей Product и Bouquet позволяет получить
        результат с аннотированными изображениями, отсортированный по полям в order_fields, и ограниченный
        параметром limit.

        :param processor: Функция, которая принимает модель, модель изображения, связанные модели,
                            список полей сортировки и лимит, и возвращает рекомендованные товары или букеты
                            с аннотированными изображениями.
        :return: NamedTuple `RecommendedItems`, содержащий два списка: рекомендованные букеты и рекомендованные продукты.
        """
        related_models = [
            RelatedModel(model="subcategory", fields=["slug", "name"]),
            RelatedModel(model="subcategory__category", fields=["slug"]),
            RelatedModel(model="tax_percent", fields=["value"]),
        ]
        recommended_bouquets = processor(
            model=Bouquet,
            image_model=BouquetImage,
            related_models=related_models,
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        recommended_products = processor(
            model=Product,
            image_model=ProductImage,
            related_models=related_models,
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        return recommended_bouquets, recommended_products

    @property
    def relative_url(self):
        return reverse_lazy("mainpage:offers")

    def get_elfsight_widget_js(self) -> None:
        cache_key = "elfsight_widget_result"
        cached_result = cache.get(cache_key)
        if cached_result is None:
            response = requests.get("https://static.elfsight.com/platform/platform.js")
            if response.status_code == 200:
                cached_result = response.text
                cache.set(cache_key, cached_result, 60 * 60 * 6)
        return cached_result


class IndividualOrderView(CreateView):
    """
    Индивидуальный заказ - форма, где пользователь оставляет свои контакты
    чтобы заказать букет из индивидуального состава. Находится между
    рекомендуемым продуктам к букетам и описанием страницы. Выглядит следующим
    образом: [ссылка](https://imgur.com/a/zbbMyNw).

    Стоит различать эту форму от той, которая находится на странице продукта.
    Форма на странице продукта называется "Индивидуальный вопрос", она
    дополнительно прикрепляет продукт, о котором идёт речь, соответствующей модели.
    """

    form_class = IndividualOrderForm
    http_method_names = ["post"]

    def form_valid(self, form: IndividualOrderForm):
        form.save(commit=True, user=self.request.user)
        return JsonResponse(
            {
                "detail": _("Мы скоро с Вами свяжемся, а пока выпейте чаю 😊"),
                "status": "success",
            },
            status=201,
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                "detail": _("Вы неправильно заполнили форму:"),
                "errors": form.errors.as_json(),
                "status": 400,
            },
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
            {
                "detail": _("Метод не разрешен. Используйте POST."),
                "status": 405,
            },
            status=405,
        )
