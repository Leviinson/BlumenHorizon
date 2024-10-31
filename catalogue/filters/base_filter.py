from django.db.models import IntegerField, Max, Min
from django.db.models.functions import Cast
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, NumberFilter, CharFilter, ChoiceFilter


class BaseFilter(FilterSet):
    aggregate_fields = []

    min_price = NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label=_("Минимальная цена"),
    )
    max_price = NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label=_("Максимальная цена"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aggregate_limits = self.get_aggregate_limits()
        self.form.fields["max_price"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "max_price_input",
                "min": 0,
                "max": self._aggregate_limits["max_price"],
                "value": self._aggregate_limits["max_price"],
            }
        )
        self.form.fields["min_price"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "min_price_input",
                "min": 0,
                "max": self._aggregate_limits["max_price"],
                "value": self._aggregate_limits["min_price"],
            }
        )

    class Meta:
        fields = [
            "price",
        ]

    def get_aggregate_limits(self):
        if not self.aggregate_fields:
            return {}

        aggregation = {
            f"min_{field}": Cast(Min(field), IntegerField())
            for field in self.aggregate_fields
        }
        aggregation.update(
            {
                f"max_{field}": Cast(Max(field), IntegerField())
                for field in self.aggregate_fields
            }
        )

        return self.Meta.model.objects.aggregate(**aggregation)
