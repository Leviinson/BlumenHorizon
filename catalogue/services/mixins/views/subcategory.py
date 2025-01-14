from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from catalogue.models import BouquetSubcategory, ProductSubcategory
from catalogue.services.mixins.views.list_mixin import ListViewMixin
from core.services.mixins.canonicals import CanonicalLinksMixin


class SubcategoryListViewMixin(ListViewMixin):
    """
    Миксин, предоставляющий общую логику для работы с подкатегориями в представлениях, отображающих либо подкатегории букетов,
    либо подкатегории продуктов.

    Этот миксин используется в классах, которые выводят список товаров в подкатегориях, обеспечивая общую логику:
    - Формирование хлебных крошек для навигации по категории и подкатегории.
    - Проверку наличия параметра `category_url_name` для правильного формирования URL в хлебных крошках.
    - Добавление мета-тегов и данных о текущей подкатегории в контекст для отображения на странице.

    Атрибуты:
        category_url_name (str): Имя URL для отображения категории в urls.py,\
            используется для формирования ссылки на категорию в хлебных крошках.

    Методы:
        get_context_data(*args, **kwargs): Собирает данные контекста для отображения страницы с подкатегориями, включая хлебные крошки и мета-теги.
    """

    category_url_name = None

    def get_context_data(self, *args, **kwargs):
        """
        Собирает и возвращает данные контекста для отображения страницы с подкатегориями.

        Этот метод:
        - Проверяет, что параметр `category_url_name` \
          установлен (это имя URL для категории в urls.py).
        - Формирует хлебные крошки для текущей подкатегории и её категории.
        - Добавляет html мета-теги, связанные с подкатегорией.
        - Добавляет данные о подкатегории в контекст.

        Возвращаемое значение:
            context: Словарь данных контекста, который будет передан в шаблон для рендеринга страницы.
        """
        context = super().get_context_data(*args, **kwargs)
        if not (self.category_url_name):
            raise ValueError(
                "Name of the category url in urls.py has to be specified",
            )
        context["breadcrumbs"] = (
            {
                "name": self.subcategory.category.name,
                "url": reverse_lazy(
                    f"catalogue:{self.category_url_name}",
                    kwargs={
                        "category_slug": self.subcategory.category.slug,
                    },
                ),
            },
            {"name": self.subcategory.name, "url": None},
        )
        context["meta_tags"] = self.subcategory.meta_tags
        context["subcategory"] = self.subcategory
        return context


class BouquetSubcategoryListViewMixin(
    SubcategoryListViewMixin,
    CanonicalLinksMixin,
):
    """
    Миксин для представления списка букетов в подкатегории.

    Этот класс:
    - Наследует `SubcategoryListViewMixin`, добавляя логику для работы с подкатегориями букетов.
    - Загружает подкатегорию букетов по слагам категории и подкатегории.
    - Фильтрует queryset товаров, относящихся только к выбранной подкатегории букетов.
    """

    category_url_name = "bouquets-category"

    def get_queryset(self):
        """
        Получает queryset для отображения подкатегории букетов.

        Этот метод:
        - Извлекает подкатегорию букетов на основе слагов категории и подкатегории.
        - Проверяет, что подкатегория существует и активна.
        - Фильтрует queryset букетов, относящихся только к этой подкатегории.

        Параметры:
            Нет дополнительных параметров, метод использует `self.kwargs` для извлечения значений слагов.

        Возвращаемое значение:
            qs: Отфильтрованный queryset товаров, принадлежащих указанной подкатегории продуктов.
        """
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            BouquetSubcategory.objects.select_related("category").only(
                "name",
                "meta_tags",
                "category__name",
                "category__slug",
                "slug",
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
            is_active=True,
        )
        return qs.filter(
            subcategory=self.subcategory,
        )

    def get_context_data(self, *args, **kwargs):
        """
        Эти параметры используются для выбора ссылок canonical/alternate
        meta-тегов.
        """
        context = super().get_context_data(*args, **kwargs)
        context["is_subcategory_list"] = True
        context["is_bouquet_subcategory"] = True
        return context

    @property
    def relative_url(self):
        return reverse_lazy(
            "catalogue:bouquets-subcategory",
            kwargs={
                "category_slug": self.subcategory.category.slug,
                "subcategory_slug": self.subcategory.slug,
            },
        )


class ProductSubcategoryListViewMixin(
    SubcategoryListViewMixin,
    CanonicalLinksMixin,
):
    """
    Миксин для представления списка продуктов в подкатегории.

    Этот класс:
    - Наследует `SubcategoryListViewMixin`, добавляя логику для работы с подкатегориями продуктов.
    - Загружает подкатегорию продуктов по слагам категории и подкатегории.
    - Фильтрует queryset товаров, относящихся только к выбранной подкатегории продуктов.

    Методы:
        get_queryset(): Извлекает и фильтрует queryset товаров, принадлежащих подкатегории продуктов.
        get_context_data(*args, **kwargs): Дополняет контекст для отображения страницы с продуктами в подкатегории.
    """

    category_url_name = "products-category"

    def get_queryset(self):
        """
        Получает queryset для отображения «стандартных товаров» в подкатегории.

        Этот метод:
        - Извлекает подкатегорию «стандартных товаров» на основе слагов категории и подкатегории.
        - Проверяет, что подкатегория существует и активна.
        - Фильтрует queryset «стандартных товаров», относящихся только к этой подкатегории.

        Параметры:
            Нет дополнительных параметров, метод использует `self.kwargs` для извлечения значений слагов.

        Возвращаемое значение:
            qs: Отфильтрованный queryset «стандартных товаров», принадлежащих указанной подкатегории «стандартных товаров».
        """

        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            ProductSubcategory.objects.select_related("category").only(
                "name",
                "meta_tags",
                "category__name",
                "category__slug",
                "slug"
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
            is_active=True,
        )
        return qs.filter(
            subcategory=self.subcategory,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_subcategory_list"] = True
        context["is_product_subcategory"] = True
        return context

    @property
    def relative_url(self):
        return reverse_lazy(
            "catalogue:products-subcategory",
            kwargs={
                "category_slug": self.subcategory.category.slug,
                "subcategory_slug": self.subcategory.slug,
            },
        )
