from django.db import transaction
from django.db.models import Prefetch
from django.db.models.manager import BaseManager
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView

from cart.cart import BouquetCart, ProductCart
from catalogue.forms import IndividualQuestionForm
from core.services.mixins import CommonContextMixin

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


class CatalogView(CommonContextMixin, TemplateView):
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

    def get_page_model(self) -> CatalogPageModel | None:
        """
        Извлекает первый объект модели `CatalogPageModel`.

        Этот метод:
        - Загружает первый объект модели `CatalogPageModel`.

        Возвращает:
            CatalogPageModel: Первый объект модели `CatalogPageModel`.
        """
        return CatalogPageModel.objects.first()


class CategoryView(CommonContextMixin, TemplateView):
    template_name = "catalog/category.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        models = (
            (BouquetCategory, BouquetSubcategory),
            (ProductCategory, ProductSubcategory),
        )
        for CategoryModel, SubcategoryModel in models:
            try:
                context["category"] = (
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
        return context


class BuyItemView(FormView):
    """
    Контроллер для добавления продукта в корзину
    и перенаправления пользователя на страницу оформления
    заказа при нажатии на кнопку "Купить" на странице
    товара.
    """

    form_class = BuyItemForm

    def form_valid(self, form):
        category_slug = form.cleaned_data["category_slug"]
        subcategory_slug = form.cleaned_data["subcategory_slug"]
        item_slug = form.cleaned_data["item_slug"]
        is_bouquet = form.cleaned_data["is_bouquet"]

        if is_bouquet:
            model_class = Bouquet
            cart_class = BouquetCart
        else:
            model_class = Product
            cart_class = ProductCart

        try:
            item = (
                model_class.objects.select_related(
                    "subcategory", "subcategory__category"
                )
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
            cart = cart_class(
                session=self.request.session, session_key=cart_class.session_key
            )
            if item not in cart.products:
                with transaction.atomic():
                    cart.add(item, item.tax_price_discounted)
                    item.amount_of_savings += 1
                    item.subcategory.amount_of_savings += 1
                    item.subcategory.save(update_fields=["amount_of_savings"])
                    item.subcategory.category.amount_of_savings += 1
                    item.subcategory.category.save(update_fields=["amount_of_savings"])
                    item.save(update_fields=["amount_of_savings"])
        except model_class.DoesNotExist:
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


class CategoryBouquetListView(BouquetCategoryListViewMixin, BouquetListView):
    pass


class SubcategoryBouquetListView(BouquetSubcategoryListViewMixin, BouquetListView):
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
