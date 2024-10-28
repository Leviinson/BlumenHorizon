from django.utils.translation import gettext_lazy as _
from django_filters import ModelMultipleChoiceFilter, NumberFilter

from ..models import Bouquet, Color, Flower
from .base_filter import BaseFilter


class BouquetFilter(BaseFilter):
    aggregate_fields = ["price", "size", "amount_of_flowers"]

    colors = ModelMultipleChoiceFilter(
        queryset=Color.objects.all(),
        field_name="colors",
        label=_("Цвета букета"),
    )
    flowers = ModelMultipleChoiceFilter(
        queryset=Flower.objects.all(),
        field_name="flowers",
        label=_("Цветы в букете"),
    )
    min_size = NumberFilter(
        field_name="size",
        lookup_expr="gte",
        label=_("Минимальный размер"),
    )
    max_size = NumberFilter(
        field_name="size",
        lookup_expr="lte",
        label=_("Максимальный размер"),
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

        self.form.fields["max_size"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "max_size_input",
                "min": self._aggregate_limits["min_size"],
                "max": self._aggregate_limits["max_size"],
                "value": self._aggregate_limits["max_size"],
            }
        )
        self.form.fields["min_size"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "min_size_input",
                "min": self._aggregate_limits["min_size"],
                "max": self._aggregate_limits["max_size"],
                "value": self._aggregate_limits["min_size"],
            }
        )

        self.form.fields["max_amount_of_flowers"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "max_amount_of_flowers_input",
                "min": self._aggregate_limits["min_amount_of_flowers"],
                "max": self._aggregate_limits["max_amount_of_flowers"],
                "value": self._aggregate_limits["max_amount_of_flowers"],
            }
        )
        self.form.fields["min_amount_of_flowers"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "min_amount_of_flowers_input",
                "min": self._aggregate_limits["min_amount_of_flowers"],
                "max": self._aggregate_limits["max_amount_of_flowers"],
                "value": self._aggregate_limits["min_amount_of_flowers"],
            }
        )

    class Meta(BaseFilter.Meta):
        model = Bouquet
        fields = BaseFilter.Meta.fields + [
            "colors",
            "flowers",
            "size",
            "amount_of_flowers",
        ]
