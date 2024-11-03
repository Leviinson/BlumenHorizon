from django.urls import path

from .views import (
    CartBouquetAddView,
    CartBouquetRemoveSingleView,
    CartBouquetRemoveView,
    CartProductAddView,
    CartProductRemoveSingleView,
    CartProductRemoveView,
    CartView,
    cart_clear,
)

app_name = "cart"
urlpatterns = (
    path("bouquet/increase/", CartBouquetAddView.as_view(), name="bouquet-add"),
    path("bouquet/remove/", CartBouquetRemoveView.as_view(), name="bouquet-remove"),
    path(
        "bouquet/decrease/",
        CartBouquetRemoveSingleView.as_view(),
        name="bouquet-remove-single",
    ),
    path(
        "product/increase/",
        CartProductAddView.as_view(),
        name="product-add",
    ),
    path(
        "product/remove/",
        CartProductRemoveView.as_view(),
        name="product-remove",
    ),
    path(
        "product/decrease/",
        CartProductRemoveSingleView.as_view(),
        name="product-remove-single",
    ),
    path("clear/", cart_clear, name="clear"),
    path("", CartView.as_view(), name="show"),
)
