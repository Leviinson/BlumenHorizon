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
from mainpage.models import SeoBlock


class SitemapMixin:
    alternates = True
    i18n = True
    x_default = True



class MainpageSitemap(SitemapMixin, Sitemap):
    priority = 1.0
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return ["mainpage:offers"]

    def location(self, item):
        return reverse_lazy(item)

    def lastmod(self, item):
        seo_block_lastmod = (
            SeoBlock.objects.only("updated_at").latest("updated_at").updated_at
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

        return max(seo_block_lastmod, product_lastmod, bouquet_lastmod)


# class ProductListSitemap(Sitemap):
#     priority = 0.5
#     protocol = "https"
#     changefreq = "weekly"

#     def items(self):
#         return ["catalogue:products-list"]

#     def location(self, item):
#         return reverse_lazy(item)

#     def lastmod(self, item):
#         return Product.objects.only("updated_at").latest("updated_at").updated_at


class ProductCategorySitemap(SitemapMixin, Sitemap):
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


class ProductSubcategorySitemap(SitemapMixin, Sitemap):
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


class ProductDetailSitemap(SitemapMixin, Sitemap):
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


# class BouquetListSitemap(SitemapMixin, Sitemap):
#     priority = 0.5
#     protocol = "https"
#     changefreq = "weekly"

#     def items(self):
#         return ["catalogue:bouquets-list"]

#     def location(self, item):
#         return reverse_lazy(item)

#     def lastmod(self, item):
#         return Bouquet.objects.only("updated_at").latest("updated_at").updated_at


class BouquetCategorySitemap(SitemapMixin, Sitemap):
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


class BouquetSubcategorySitemap(SitemapMixin, Sitemap):
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


class BouquetDetailSitemap(SitemapMixin, Sitemap):
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
