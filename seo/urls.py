from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path


from .sitemaps import (
    MainpageSitemap,
    BouquetCategorySitemap,
    BouquetDetailSitemap,
    BouquetListSitemap,
    BouquetSubcategorySitemap,
    ProductCategorySitemap,
    ProductDetailSitemap,
    ProductListSitemap,
    ProductSubcategorySitemap,
)
from .views import robots_txt

sitemaps = {
    "mainpage": MainpageSitemap,
    "products-list": ProductListSitemap,
    "products-category": ProductCategorySitemap,
    "products-subcategory": ProductSubcategorySitemap,
    "product-details": ProductDetailSitemap,
    "bouquets-list": BouquetListSitemap,
    "bouquets-category": BouquetCategorySitemap,
    "bouquets-subcategory": BouquetSubcategorySitemap,
    "bouquet-details": BouquetDetailSitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", robots_txt, name="robots-txt"),
]
