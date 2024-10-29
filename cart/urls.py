from django.urls import path

from .views import CartItemAdd, CartItemRemove, cart_clear

app_name = "cart"
urlpatterns = (
    path("add/", CartItemAdd.as_view(), name="add"),
    path("remove/", CartItemRemove.as_view(), name="remove"),
    path("clear/", cart_clear, name="clear"),
    # path("", CartView.as_view(), name="show"),
)
