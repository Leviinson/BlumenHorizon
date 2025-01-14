from django.db import transaction
from django.db.models import Prefetch
from django.db.models.manager import BaseManager
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView

from cart.cart import BouquetCart, ProductCart
from catalogue.forms import IndividualQuestionForm
from core.services.mixins import CanonicalsContextMixin, CommonContextMixin
from core.services.mixins.canonicals import CanonicalLinksMixin

from ..forms import BuyItemForm
from ..models import (
    Bouquet,
    BouquetCategory,
    BouquetSubcategory,
    CatalogPageModel,
    Product,
    ProductCategory,
    ProductSubcategory,
)
from ..services.mixins.views.category import (
    BouquetCategoryListViewMixin,
    ProductCategoryListViewMixin,
)
from ..services.mixins.views.subcategory import (
    BouquetSubcategoryListViewMixin,
    ProductSubcategoryListViewMixin,
)
from .bouquets import BouquetListView
from .products import ProductListView


class CatalogView(
    CommonContextMixin,
    CanonicalsContextMixin,
    CanonicalLinksMixin,
    TemplateView,
):
    """
    Представление каталога, отображающее список категорий и их подкатегорий
      для букетов и продуктов.

    Этот класс:
    - Загружает и отображает активные категории букетов и продуктов.
    - Формирует данные для контекста, включая информацию о подкатегориях
    и html мета-тегах страницы.
    - Использует методы для извлечения категорий и подкатегорий,а также
    для получения html мета-информации страницы.

    Атрибуты:
        template_name (str): Имя шаблона, который используется для рендеринга страницы каталога.
        http_method_names (list): Список разрешённых HTTP-методов для этого представления.
        В данном случае только "get".
    """

    template_name = "catalog/catalog.html"
    http_method_names = ["get"]

    def get_context_data(self, *args, **kwargs):
        """
        Собирает данные контекста для страницы каталога.

        Этот метод:
        - Извлекает категории букетов и продуктов.
        - Загружает мета-теги и описание страницы каталога.
        - Формирует словарь данных для рендеринга страницы.

        Аргументы:
            *args, **kwargs: Дополнительные аргументы и параметры, передаваемые в родительский метод.

        Возвращает:
            dict: Контекст для рендеринга страницы.
        """
        context = super().get_context_data(*args, **kwargs)
        context["bouquets_categories"] = self.get_bouquet_categories()
        context["products_categories"] = self.get_product_categories()

        page_model = self.get_page_model()
        context["meta_tags"] = page_model.meta_tags
        context["description"] = page_model.description
        return context

    def get_page_model(self) -> CatalogPageModel | None:
        """
        Извлекает первый объект модели `CatalogPageModel`.

        Этот метод:
        - Загружает первый объект модели `CatalogPageModel`.

        Возвращает:
            CatalogPageModel: Первый объект модели `CatalogPageModel`.
        """
        return CatalogPageModel.objects.first()

    def get_bouquet_categories(self) -> BaseManager[BouquetCategory]:
        """
        Извлекает активные категории букетов с подкатегориями.

        Этот метод:
        - Загружает категории букетов с активными подкатегориями.
        - Использует Prefetch для предварительной загрузки подкатегорий.

        Возвращает:
            QuerySet: Список активных категорий букетов с подкатегориями.
        """
        return (
            BouquetCategory.objects.prefetch_related(
                Prefetch(
                    "subcategories",
                    queryset=BouquetSubcategory.objects.filter(is_active=True),
                )
            )
            .only(
                "name",
                "slug",
                "image",
                "image_alt",
                "subcategories__name",
                "subcategories__slug",
                "subcategories__image",
                "subcategories__image_alt",
            )
            .filter(is_active=True)
        )

    def get_product_categories(self) -> BaseManager[ProductCategory]:
        """
        Извлекает активные категории продуктов с подкатегориями.

        Этот метод:
        - Загружает категории продуктов с активными подкатегориями.
        - Использует Prefetch для предварительной загрузки подкатегорий.

        Возвращает:
            QuerySet: Список активных категорий продуктов с подкатегориями.
        """
        return (
            ProductCategory.objects.prefetch_related(
                Prefetch(
                    "subcategories",
                    queryset=ProductSubcategory.objects.filter(is_active=True),
                )
            )
            .only(
                "name",
                "slug",
                "image",
                "image_alt",
                "subcategories__name",
                "subcategories__slug",
                "subcategories__image",
                "subcategories__image_alt",
            )
            .filter(is_active=True)
        )

    @property
    def relative_url(self) -> str:
        return reverse_lazy("catalogue:catalog")


class CategoryView(
    CommonContextMixin,
    CanonicalLinksMixin,
    CanonicalsContextMixin,
    TemplateView,
):
    template_name = "catalog/category.html"

    def get_context_data(self, *args, **context):
        models = (
            (BouquetCategory, BouquetSubcategory),
            (ProductCategory, ProductSubcategory),
        )
        for CategoryModel, SubcategoryModel in models:
            try:
                self.object = context["category"] = (
                    CategoryModel.objects.prefetch_related(
                        Prefetch(
                            "subcategories",
                            queryset=SubcategoryModel.objects.filter(is_active=True),
                        )
                    )
                    .only(
                        "name",
                        "slug",
                        "image",
                        "image_alt",
                        "description",
                        "subcategories__name",
                        "subcategories__slug",
                        "subcategories__image",
                        "subcategories__image_alt",
                        "code_value",
                        "catalog_page_meta_tags",
                    )
                    .filter(is_active=True)
                    .get(slug=self.kwargs["category_slug"])
                )
                break
            except CategoryModel.DoesNotExist:
                continue
        else:
            raise Http404()
        context["meta_tags"] = context["category"].catalog_page_meta_tags
        context["description"] = context["category"].description
        return super().get_context_data(*args, **context)

    @property
    def relative_url(self):
        return reverse_lazy(
            "catalogue:category",
            kwargs={
                "category_slug": self.object.slug,
            },
        )


class BuyItemView(FormView):
    """
    Контроллер для добавления продукта в корзину
    и перенаправления пользователя на страницу оформления
    заказа при нажатии на кнопку "Купить" на странице
    товара.
    """

    form_class = BuyItemForm
    http_method_names = [
        "post",
    ]

    def _get_model_and_cart_classes(
        self,
        item_slug: str,
    ) -> tuple[Product | Bouquet, ProductCart | BouquetCart]:
        """
        Определяет модель и класс корзины по слагу продукта.

        :param item_slug: Слаг продукта.
        :return: Кортеж (model_class, cart_class).
        :raises Http404: Если продукт не найден.
        """
        if Bouquet.objects.filter(slug=item_slug).exists():
            return Bouquet, BouquetCart
        elif Product.objects.filter(slug=item_slug).exists():
            return Product, ProductCart
        raise Http404(
            _("Данный продукт был недавно удалён из каталога нашими администраторами")
        )

    def _get_item(
        self,
        model_class: Product | Bouquet,
        category_slug: str,
        subcategory_slug: str,
        item_slug: str,
    ) -> Product | Bouquet:
        """
        Получает объект продукта из базы данных.

        :param model_class: Класс модели продукта (Bouquet или Product).
        :param category_slug: Слаг категории продукта.
        :param subcategory_slug: Слаг подкатегории продукта.
        :param item_slug: Слаг продукта.
        :return: Объект продукта.
        :raises model_class.DoesNotExist: Если продукт не найден.
        """
        return (
            model_class.objects.select_related("subcategory", "subcategory__category")
            .only(
                "price",
                "discount",
                "amount_of_savings",
                "subcategory__amount_of_savings",
                "subcategory__category__amount_of_savings",
            )
            .get(
                slug=item_slug,
                is_active=True,
                subcategory__slug=subcategory_slug,
                subcategory__category__slug=category_slug,
            )
        )

    def _update_savings(self, item: Product | Bouquet) -> None:
        """
        Обновляет счётчики сохранений в корзине для
        продукта, подкатегории и категории.

        :param item: Объект продукта.
        """
        with transaction.atomic():
            item.amount_of_savings += 1
            item.subcategory.amount_of_savings += 1
            item.subcategory.category.amount_of_savings += 1
            item.save(update_fields=["amount_of_savings"])
            item.subcategory.save(update_fields=["amount_of_savings"])
            item.subcategory.category.save(update_fields=["amount_of_savings"])

    def _add_item_to_cart(
        self, cart: ProductCart | BouquetCart, item: Product | Bouquet
    ) -> None:
        """
        Добавляет продукт в корзину, если его ещё нет.

        :param cart: Экземпляр корзины.
        :param item: Объект продукта.
        """
        if item not in cart.products:
            cart.add(item, item.tax_price_discounted)

    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Обрабатывает данные формы для добавления продукта в корзину.

        :param form: Валидированная форма.
        :return: Перенаправление на страницу корзины.
        """
        category_slug = form.cleaned_data["category_slug"]
        subcategory_slug = form.cleaned_data["subcategory_slug"]
        item_slug = form.cleaned_data["item_slug"]

        ItemModel, Cart = self._get_model_and_cart_classes(item_slug)
        try:
            item = self._get_item(ItemModel, category_slug, subcategory_slug, item_slug)
            cart = Cart(session=self.request.session, session_key=Cart.session_key)
            self._add_item_to_cart(cart, item)
            self._update_savings(item)
        except ItemModel.DoesNotExist:
            raise Http404(
                _(
                    "Данный продукт был недавно удалён из каталога нашими администраторами"
                )
            )

        return redirect("cart:show")

    def form_invalid(self, form):
        return redirect("mainpage:offers")


class CategoryProductsListView(ProductCategoryListViewMixin, ProductListView):
    pass


class SubcategoryProductsListView(ProductSubcategoryListViewMixin, ProductListView):
    pass


class CategoryBouquetsListView(BouquetCategoryListViewMixin, BouquetListView):
    pass


class SubcategoryBouquetsListView(BouquetSubcategoryListViewMixin, BouquetListView):
    pass


class IndividualQuestionView(CreateView):
    form_class = IndividualQuestionForm
    http_method_names = ["post"]

    def form_valid(self, form: IndividualQuestionForm):
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
                "detail": _("Ошибка:"),
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
