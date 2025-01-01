from typing import Any

from django.db.models.manager import BaseManager
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from cart.cart import BouquetCart, ProductCart
from catalogue.forms import IndividualQuestionForm
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.dataclasses import RelatedModel
from core.services.utils import get_recommended_items_with_first_image


class DetailViewMixin:
    """
    Миксин для отображения страницы товара.

    Применяется для BouquetView и ProductView.

    :param category_url_name: название path() в urls.py для контроллера, который
    отображает список продуктов в категории продукта. Используется для
    построения хлебных крошек
    :param subcategory_url_name: название path() в urls.py для контроллера, который
    отображает список продуктов в подкатегории продукта. Используется для
    построения хлебных крошек
    :param cart: Класс корзины, которая хранит этот тип продукта. ProductCart для
    стандартных продуктов, BouquetCart для букетов.
    :param model: Модель, которая представляет собой тип продукта. Product для
    стандартных продуктов, Bouquet для букетов.
    :param image_model: Модель, которая хранит фотографии для данного типа продукта.
    ProductImage для стандартных продуктов, BouquetImage для букетов.
    """

    category_url_name: str
    subcategory_url_name: str
    cart: type[ProductCart] | type[BouquetCart]
    model: type[Product] | type[Bouquet]
    image_model: type[ProductImage] | type[BouquetImage]

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """
        Получает данные контекста для отображения.

        Возвращает словарь с данными, необходимыми для шаблона.
        """
        self._validate_category_urls()
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                "meta_tags": self._get_meta_tags(),
                "breadcrumbs": self._get_breadcrumbs(),
                "individual_question_form": self._get_individual_question_form(),
                "cart": self._get_cart(),
                "recommended_products": self._get_recommended_products(),
            }
        )
        return context

    def _validate_category_urls(self) -> None:
        """
        Проверяет, что category_url_name и subcategory_url_name указаны.

        Вызывает исключение ValueError, если они отсутствуют.
        """
        if not (self.category_url_name and self.subcategory_url_name):
            raise ValueError(
                "Category url and subcategory url name from urls.py must be specified."
            )

    def _get_meta_tags(self) -> Any:
        """
        Возвращает html мета-теги текущего товара.

        :return: мета-теги товара.
        """
        return self.object.meta_tags

    def _get_breadcrumbs(self) -> list[dict[str, Any]]:
        """
        Формирует и возвращает данные для хлебных крошек.

        :return: список словарей с именем и URL для каждого шага.
        """
        return [
            {
                "name": self.object.subcategory.category.name,
                "url": reverse_lazy(
                    f"catalogue:{self.category_url_name}",
                    kwargs={"category_slug": self.object.subcategory.category.slug},
                ),
            },
            {
                "name": self.object.subcategory.name,
                "url": reverse_lazy(
                    f"catalogue:{self.subcategory_url_name}",
                    kwargs={
                        "category_slug": self.object.subcategory.category.slug,
                        "subcategory_slug": self.object.subcategory.slug,
                    },
                ),
            },
            {"name": self.object.name, "url": None},
        ]

    def _get_individual_question_form(self) -> IndividualQuestionForm:
        """
        Возвращает форму для индивидуального вопроса
        о продукте.

        :return: экземпляр IndividualQuestionForm.
        """
        return IndividualQuestionForm()

    def _get_cart(self) -> ProductCart | BouquetCart:
        """
        Возвращает корзину пользователя из сессии.

        :return: объект корзины.
        """
        return self.cart(
            session=self.request.session, session_key=self.cart.session_key
        )

    def _get_recommended_products(self) -> BaseManager[Product | Bouquet]:
        """
        Получает список рекомендованных продуктов с первым изображением.

        :return: список рекомендованных продуктов.
        """
        related_models = [
            RelatedModel(model="subcategory", fields=["slug", "name"]),
            RelatedModel(model="subcategory__category", fields=["slug"]),
        ]
        return get_recommended_items_with_first_image(
            model=self.model,
            image_model=self.image_model,
            related_models=related_models,
            order_fields=["-amount_of_orders", "-amount_of_savings"],
        )

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        if not (self.category_url_name and self.subcategory_url_name):
            raise ValueError(
                "Category url and subcategory url name from urls.py must be specified."
            )
        context = super().get_context_data(*args, **kwargs)
        context["meta_tags"] = self.object.meta_tags
        context["breadcrumbs"] = [
            {
                "name": self.object.subcategory.category.name,
                "url": reverse_lazy(
                    f"catalogue:{self.category_url_name}",
                    kwargs={
                        "category_slug": self.object.subcategory.category.slug,
                    },
                ),
            },
            {
                "name": self.object.subcategory.name,
                "url": reverse_lazy(
                    f"catalogue:{self.subcategory_url_name}",
                    kwargs={
                        "category_slug": self.object.subcategory.category.slug,
                        "subcategory_slug": self.object.subcategory.slug,
                    },
                ),
            },
            {"name": self.object.name, "url": None},
        ]
        context["individual_question_form"] = IndividualQuestionForm()
        context["cart"] = self.cart(
            session=self.request.session, session_key=self.cart.session_key
        )
        related_models = [
            RelatedModel(model="subcategory", fields=["slug", "name"]),
            RelatedModel(model="subcategory__category", fields=["slug"]),
        ]
        context["recommended_products"] = get_recommended_items_with_first_image(
            model=self.model,
            image_model=self.image_model,
            related_models=related_models,
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get(
                subcategory__category__slug=self.kwargs["category_slug"],
                subcategory__slug=self.kwargs["subcategory_slug"],
                slug=self.kwargs[self.slug_url_kwarg],
            )
        except queryset.model.DoesNotExist:
            raise Http404(
                _("Не найдено ни одного %(verbose_name)s совпадающего по запросу")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
