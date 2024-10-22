from django.urls import path

from ..views import BouquetListView, BouquetView

app_name = "bouquets"

urlpatterns = [
    path("", BouquetListView.as_view(), name="list"),
    path("<slug:bouquet_slug>/", BouquetView.as_view(), name="detail"),
]