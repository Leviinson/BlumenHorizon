from django.urls import path

from ..views import ProductListView, ProductView

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<slug:product_slug>/", ProductView.as_view(), name="detail"),
]