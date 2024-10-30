from django.urls import path

from .views import (
    CartBouquetAdd,
    CartBouquetRemove,
    CartProductAdd,
    CartProductRemove,
    CartView,
    cart_clear,
)

app_name = "cart"
urlpatterns = (
    path("bouquet/add/", CartBouquetAdd.as_view(), name="bouquet-add"),
    path("bouquet/remove/", CartBouquetRemove.as_view(), name="bouquet-remove"),
    path("product/add/", CartProductAdd.as_view(), name="product-add"),
    path("product/remove/", CartProductRemove.as_view(), name="product-remove"),
    path("clear/", cart_clear, name="clear"),
    path("", CartView.as_view(), name="show"),
)
