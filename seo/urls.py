from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import (
    AboutUsSitemap,
    BouquetCategorySitemap,
    BouquetDetailSitemap,
    BouquetSubcategorySitemap,
    ContactSitemap,
    DeliverySitemap,
    MainpageSitemap,
)
from .views import robots_txt

sitemaps = {
    "mainpage": MainpageSitemap,
    # "products-list": ProductListSitemap,
    # "products-category": ProductCategorySitemap,
    # "products-subcategory": ProductSubcategorySitemap,
    # "product-details": ProductDetailSitemap,
    # "bouquets-list": BouquetListSitemap,
    "bouquets-category": BouquetCategorySitemap,
    "bouquets-subcategory": BouquetSubcategorySitemap,
    "bouquet-details": BouquetDetailSitemap,
    # "faq": FAQSitemap,
    "delivery": DeliverySitemap,
    "contacts": ContactSitemap,
    "about-us": AboutUsSitemap,
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
