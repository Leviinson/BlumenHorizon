from django.contrib.sitemaps import Sitemap
from django.db.models import Max
from django.urls import reverse_lazy
from django.utils import translation

from catalogue.models import (
    Bouquet,
    BouquetCategory,
    BouquetSubcategory,
    Product,
    ProductCategory,
    ProductSubcategory,
)
from mainpage.models import (
    AboutUsPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    MainPageSeoBlock,
)
from datetime import datetime


class FixedSitemapMixin(Sitemap):
    alternates = True
    i18n = True
    x_default = True

    def _location(self, item, force_lang_code=None):
        if self.i18n:
            obj, lang_code = item
            # Activate language from item-tuple or forced one before calling location.
            with translation.override(force_lang_code or lang_code):
                return str(
                    self._get("location", item)
                )  # It was wrapped in str(), since it fixes bug
                # when it generates alternates without
                # language code specifying
        return self._get("location", item)


class MainpageSitemap(FixedSitemapMixin):
    priority = 1.0
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return ["mainpage:offers"]

    def location(self, item):
        return reverse_lazy(item)

    def lastmod(self, item):
        seo_block_lastmod = (
            MainPageSeoBlock.objects.only("updated_at").latest("updated_at").updated_at
        )

        product_lastmod = (
            Product.objects.filter(
                is_active=True,
                subcategory__is_active=True,
                subcategory__category__is_active=True,
            )
            .only(
                "updated_at",
                "amount_of_orders",
                "amount_of_savings",
            )
            .order_by("-amount_of_orders", "-amount_of_savings")[:12]
            .aggregate(Max("updated_at"))["updated_at__max"]
        )

        bouquet_lastmod = (
            Bouquet.objects.filter(
                is_active=True,
                subcategory__is_active=True,
                subcategory__category__is_active=True,
            )
            .only(
                "updated_at",
                "amount_of_orders",
                "amount_of_savings",
            )
            .order_by("-amount_of_orders", "-amount_of_savings")[:12]
            .aggregate(Max("updated_at"))["updated_at__max"]
        )

        return max(
            filter(None, [seo_block_lastmod, bouquet_lastmod, product_lastmod]),
            default=datetime.min,
        )


# class ProductListSitemap(FixedSitemapMixin):
#     priority = 0.5
#     protocol = "https"
#     changefreq = "weekly"

#     def items(self):
#         return ["catalogue:products-list"]

#     def location(self, item):
#         return reverse_lazy(item)

#     def lastmod(self, item):
#         return Product.objects.only("updated_at").latest("updated_at").updated_at


class ProductCategorySitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return ProductCategory.objects.only(
            "slug",
            "amount_of_orders",
            "amount_of_savings",
        ).order_by("-amount_of_orders", "-amount_of_savings")

    def location(self, item: ProductCategory):
        return item.get_relative_url()

    def lastmod(self, item: ProductCategory):
        return (
            Product.objects.select_related(
                "subcategory__category",
                "subcategory",
            )
            .only("updated_at", "subcategory__category__id", "subcategory__id")
            .filter(subcategory__category=item)
            .latest("updated_at")
            .updated_at
        )


class ProductSubcategorySitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return (
            ProductSubcategory.objects.select_related("category")
            .annotate(lastmod=Max("products__updated_at"))
            .only(
                "slug",
                "category__slug",
                "amount_of_orders",
                "amount_of_savings",
            )
            .order_by("-amount_of_orders", "-amount_of_savings")
        )

    def location(self, item: ProductSubcategory):
        return item.get_relative_url()

    def lastmod(self, item: ProductSubcategory):
        return item.lastmod


class ProductDetailSitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return (
            Product.objects.select_related("subcategory", "subcategory__category")
            .only(
                "slug",
                "subcategory__slug",
                "subcategory__category__slug",
                "updated_at",
                "amount_of_orders",
                "amount_of_savings",
            )
            .order_by("-amount_of_orders", "-amount_of_savings")
        )

    def location(self, item: Product):
        return item.get_relative_url()

    def lastmod(self, item: Product):
        return item.updated_at


# class BouquetListSitemap(FixedSitemapMixin):
#     priority = 0.5
#     protocol = "https"
#     changefreq = "weekly"

#     def items(self):
#         return ["catalogue:bouquets-list"]

#     def location(self, item):
#         return reverse_lazy(item)

#     def lastmod(self, item):
#         return Bouquet.objects.only("updated_at").latest("updated_at").updated_at


class BouquetCategorySitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return BouquetCategory.objects.only(
            "slug",
            "updated_at",
            "amount_of_orders",
            "amount_of_savings",
        ).order_by("-amount_of_orders", "-amount_of_savings")

    def location(self, item: BouquetCategory):
        return item.get_relative_url()

    def lastmod(self, item: BouquetCategory):
        qs = (
            Bouquet.objects.select_related(
                "subcategory__category",
                "subcategory",
            )
            .only(
                "updated_at",
                "subcategory__category__id",
                "subcategory__id",
                "amount_of_orders",
                "amount_of_savings",
            )
            .filter(subcategory__category=item)
        )
        if qs.exists():
            return qs.latest("updated_at").updated_at


class BouquetSubcategorySitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return (
            BouquetSubcategory.objects.select_related("category")
            .annotate(lastmod=Max("bouquets__updated_at"))
            .only(
                "slug",
                "category__slug",
                "bouquets__updated_at",
                "amount_of_orders",
                "amount_of_savings",
            )
            .order_by("-amount_of_orders", "-amount_of_savings")
        )

    def location(self, item: BouquetSubcategory):
        return item.get_relative_url()

    def lastmod(self, item: BouquetSubcategory):
        return item.lastmod


class BouquetDetailSitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return (
            Bouquet.objects.select_related("subcategory", "subcategory__category")
            .only(
                "slug",
                "subcategory__slug",
                "subcategory__category__slug",
                "updated_at",
                "amount_of_orders",
                "amount_of_savings",
            )
            .order_by("-amount_of_orders", "-amount_of_savings")
        )

    def location(self, item: Bouquet):
        return item.get_relative_url()

    def lastmod(self, item: Bouquet):
        return item.updated_at


class FAQSitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return FAQPageModel.objects.only("updated_at")

    def location(self, item: Bouquet):
        return reverse_lazy("mainpage:faq")

    def lastmod(self, item: Bouquet):
        return item.updated_at


class AboutUsSitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return AboutUsPageModel.objects.only("updated_at")

    def location(self, item: Bouquet):
        return reverse_lazy("mainpage:about")

    def lastmod(self, item: Bouquet):
        return item.updated_at


class DeliverySitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return DeliveryPageModel.objects.only("updated_at")

    def location(self, item: Bouquet):
        return reverse_lazy("mainpage:delivery")

    def lastmod(self, item: Bouquet):
        return item.updated_at


class ContactSitemap(FixedSitemapMixin):
    priority = 0.5
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return ContactsPageModel.objects.only("updated_at")

    def location(self, item: Bouquet):
        return reverse_lazy("mainpage:contact")

    def lastmod(self, item: Bouquet):
        return item.updated_at
