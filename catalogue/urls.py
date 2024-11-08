from django.urls import path

from catalogue.views.catalogue import IndividualQuestionView

from .views import (
    BouquetListView,
    BouquetView,
    CategoryBouquetListView,
    CategoryProductsListView,
    ProductListView,
    ProductView,
    SubcategoryBouquetListView,
    SubcategoryProductsListView,
)

app_name = "catalogue"

urlpatterns = [
    path("individual-question/",
         IndividualQuestionView.as_view(),
         name="individual-question"),
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
        "products/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/",
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
        CategoryBouquetListView.as_view(),
        name="bouquets-category",
    ),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/",
        SubcategoryBouquetListView.as_view(),
        name="bouquets-subcategory",
    ),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/<slug:bouquet_slug>/",
        BouquetView.as_view(),
        name="bouquet-details",
    ),
]
