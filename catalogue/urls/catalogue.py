from django.urls import path

from ..views import CategoryProductsListView, SubcategoryProductsListView

app_name = "catalogue"

urlpatterns = [
    path("<slug:category_slug>/", CategoryProductsListView.as_view(), name="category"),
    path("<slug:category_slug>/<slug:subcategory_slug>/", SubcategoryProductsListView.as_view(), name="subcategory")
]