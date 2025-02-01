from typing import NamedTuple

from django.db.models.manager import BaseManager

from catalogue.models import Bouquet, BouquetCategory, Product, ProductCategory


class RecommendedItems(NamedTuple):
    recommended_bouquets: BaseManager[Bouquet]
    recommended_products: BaseManager[Product]


class Categories(NamedTuple):
    products_categories: BaseManager[ProductCategory]
    bouquets_categories: BaseManager[BouquetCategory]
