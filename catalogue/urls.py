from django.urls import path

from .views import (
    BouquetListView,
    BouquetView,
    CategoryProductsListView,
    ProductListView,
    ProductView,
    SubcategoryProductsListView,
)

app_name = "catalogue"

urlpatterns = [
    path(
        "products/",
        ProductListView.as_view(),
        name="products-list",
    ),
    path(
        "products/<slug:category_slug>/",
        CategoryProductsListView.as_view(),
        name="products-category",
    ),
    path(
        "products/<slug:category_slug>/<slug:subcategory_slug>/",
        SubcategoryProductsListView.as_view(),
        name="products-subcategory",
    ),
    path(
        "products/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>",
        ProductView.as_view(),
        name="product-details",
    ),
    path(
        "bouquets/",
        BouquetListView.as_view(),
        name="bouquets-list",
    ),
    path(
        "bouquets/<slug:category_slug>/",
        CategoryProductsListView.as_view(),
        name="bouquets-category",
    ),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/",
        SubcategoryProductsListView.as_view(),
        name="bouquets-subcategory",
    ),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/<slug:bouquet_slug>",
        BouquetView.as_view(),
        name="bouquet-details",
    ),
]
