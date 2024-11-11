from django.urls import path

from .views import live_search

app_name = "live-search"

urlpatterns = [path("", live_search, name="search")]
