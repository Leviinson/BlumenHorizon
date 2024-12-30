from ..models import Product
from .base_filter import BaseFilter


class ProductFilter(BaseFilter):
    aggregate_fields = [
        "price",
    ]

    class Meta(BaseFilter.Meta):
        model = Product
