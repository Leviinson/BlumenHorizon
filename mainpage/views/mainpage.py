from typing import Any

from django.db.models.manager import BaseManager
from django.http import JsonResponse
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
from core.services.mixins.views import CommonContextMixin
from core.services.utils import get_carts, get_recommended_items_with_first_image

from ..forms import IndividualOrderForm
from ..models import MainPageModel, MainPageSeoBlock, MainPageSliderImages


class MainPageView(CommonContextMixin, TemplateView):
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

        base_context["recommended_bouquets"],
        base_context["recommended_products"] = self.get_recommended_items()

        base_context["products_cart"],
        base_context["bouquets_cart"] = get_carts(self.request.session)

        base_context["products_categories"],
        base_context["bouquets_categories"] = self.get_categories_tuple()

        base_context["individual_order_form"] = IndividualOrderForm()
        base_context["seo_block"] = MainPageSeoBlock.objects.first()
        base_context["description"] = page_model.description

        page_model = MainPageModel.objects.first()
        base_context["meta_tags"] = page_model.meta_tags
        base_context["json_ld_description"] = page_model.json_ld_description
        return base_context

    @staticmethod
    def get_categories_tuple() -> (
        tuple[BaseManager[ProductCategory], BaseManager[BouquetCategory]]
    ):
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
    def get_recommended_items() -> tuple[
        BaseManager[Product] | BaseManager[Bouquet],
        BaseManager[Product] | BaseManager[Bouquet],
    ]:
        """
        Возвращает рекомендованные букеты и продукты используя функцию,
        выполняющую роль фабрики.

        Используется для слайдеров «Рекомендованные букеты к покупке» и
        «Рекомендуемые подарки к букетам» на главной странице, а так-же
        для секций «Рекомендуемые букеты к покупке» и
        «Рекомендуемые подарки к букетам» на странице корзины пользователя."
        """
        related_models = [
            RelatedModel(model="subcategory", attributes=["slug", "name"]),
            RelatedModel(model="subcategory__category", attributes=["slug"]),
        ]
        recommended_bouquets = get_recommended_items_with_first_image(
            model=Bouquet,
            image_model=BouquetImage,
            related_models=related_models,
            image_filter_field="bouquet",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        recommended_products = get_recommended_items_with_first_image(
            model=Product,
            image_model=ProductImage,
            related_models=related_models,
            image_filter_field="product",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        return recommended_bouquets, recommended_products


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
