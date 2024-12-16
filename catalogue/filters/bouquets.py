from django.utils.translation import gettext_lazy as _
from django_filters import CharFilter, NumberFilter

from ..models import Bouquet
from .base_filter import BaseFilter


class BouquetFilter(BaseFilter):
    aggregate_fields = ["price", "diameter", "amount_of_flowers"]

    colors = CharFilter(
        method="filter_by_colors",
        label=_("Цветовая гамма букета"),
    )
    flowers = CharFilter(
        method="filter_by_flowers",
        label=_("Состав"),
    )
    min_diameter = NumberFilter(
        field_name="diameter",
        lookup_expr="gte",
        label=_("Минимальный диаметр букета"),
    )
    max_diameter = NumberFilter(
        field_name="diameter",
        lookup_expr="lte",
        label=_("Максимальный диаметр букета"),
    )
    min_amount_of_flowers = NumberFilter(
        field_name="amount_of_flowers",
        lookup_expr="gte",
        label=_("Минимальное количество цветов в букете"),
    )
    max_amount_of_flowers = NumberFilter(
        field_name="amount_of_flowers",
        lookup_expr="lte",
        label=_("Максимальное количество цветов в букете"),
    )

    min_price = NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label=_("Минимальная цена"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["max_diameter"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "max_diameter_input",
                "min": 0,
                "max": self._aggregate_limits["max_diameter"],
                "value": self._aggregate_limits["max_diameter"],
            }
        )
        self.form.fields["min_diameter"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "min_diameter_input",
                "min": 0,
                "max": self._aggregate_limits["max_diameter"],
                "value": self._aggregate_limits["min_diameter"],
            }
        )

        self.form.fields["max_amount_of_flowers"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "max_amount_of_flowers_input",
                "min": 0,
                "max": self._aggregate_limits["max_amount_of_flowers"],
                "value": self._aggregate_limits["max_amount_of_flowers"],
            }
        )
        self.form.fields["min_amount_of_flowers"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "min_amount_of_flowers_input",
                "min": 0,
                "max": self._aggregate_limits["max_amount_of_flowers"],
                "value": self._aggregate_limits["min_amount_of_flowers"],
            }
        )

    class Meta(BaseFilter.Meta):
        model = Bouquet
        fields = BaseFilter.Meta.fields + [
            "colors",
            "flowers",
            "diameter",
            "amount_of_flowers",
        ]

    def filter_by_colors(self, queryset, name: str, value: str):
        if value:
            color_names = value.split(",")
            queryset = queryset.filter(colors__name__in=color_names).distinct()
        return queryset

    def filter_by_flowers(self, queryset, name: str, value: str):
        if value:
            flower_names = value.split(",")
            queryset = queryset.filter(flowers__name__in=flower_names).distinct()
        return queryset
