from django.urls import path

from .views import (
    CartBouquetAdd,
    CartBouquetRemove,
    CartBouquetRemoveSingle,
    CartProductAdd,
    CartProductRemove,
    CartProductRemoveSingle,
    CartView,
    cart_clear,
)

app_name = "cart"
urlpatterns = (
    path("bouquet/increase/", CartBouquetAdd.as_view(), name="bouquet-add"),
    path("bouquet/remove/", CartBouquetRemove.as_view(), name="bouquet-remove"),
    path("bouquet/decrease/", CartBouquetRemoveSingle.as_view(), name="bouquet-remove-single"),
    path("product/increase/", CartProductAdd.as_view(), name="product-add"),
    path("product/remove/", CartProductRemove.as_view(), name="product-remove"),
    path("product/decrease/", CartProductRemoveSingle.as_view(), name="product-remove-single"),
    path("clear/", cart_clear, name="clear"),
    path("", CartView.as_view(), name="show"),
)
