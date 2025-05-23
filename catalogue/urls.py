from django.urls import path

from catalogue.views.catalogue import IndividualQuestionView

from .views import (
    BouquetView,
    BuyItemView,
    CatalogView,
    CategoryBouquetsListView,
    CategoryProductsListView,
    CategoryView,
    CreateBouquetReviewView,
    CreateProductReviewView,
    ProductView,
    SubcategoryBouquetsListView,
    SubcategoryProductsListView,
)

app_name = "catalogue"

urlpatterns = [
    path(
        "",
        CatalogView.as_view(),
        name="catalog",
    ),
    path(
        "category/<slug:category_slug>/",
        CategoryView.as_view(),
        name="category",
    ),
    path(
        "individual-question/",
        IndividualQuestionView.as_view(),
        name="individual-question",
    ),
    # path(
    #     "products/",
    #     ProductListView.as_view(),
    #     name="products-list",
    # ),
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
        "products/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/reviews/",
        CreateProductReviewView.as_view(),
        name="product-review",
    ),
    # path(
    #     "bouquets/",
    #     BouquetListView.as_view(),
    #     name="bouquets-list",
    # ),
    path(
        "bouquets/<slug:category_slug>/",
        CategoryBouquetsListView.as_view(),
        name="bouquets-category",
    ),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/",
        SubcategoryBouquetsListView.as_view(),
        name="bouquets-subcategory",
    ),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/<slug:bouquet_slug>/",
        BouquetView.as_view(),
        name="bouquet-details",
    ),
    # path(
    #     "bouquets/<slug:category_slug>/<slug:subcategory_slug>/<slug:bouquet_slug>/sizes/",
    #     GetBouquetSizes.as_view(),
    #     name="get-bouquet-sizes",
    # ),
    path("buy/", BuyItemView.as_view(), name="buy-item"),
    path(
        "bouquets/<slug:category_slug>/<slug:subcategory_slug>/<slug:bouquet_slug>/reviews/",
        CreateBouquetReviewView.as_view(),
        name="bouquet-review",
    ),
]
