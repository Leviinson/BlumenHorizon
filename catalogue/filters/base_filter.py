from django import forms
from django.db.models import IntegerField, Max, Min
from django.db.models.functions import Cast
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, NumberFilter


class EnabledBooleanFilter(BooleanFilter):
    __field_class = forms.NullBooleanField
    __field_class.initial = True
    field_class = __field_class


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
    with_discount = EnabledBooleanFilter(
        label=_("Со скидкой"),
        field_name="discount",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input checkbox-dark"}),
        method="filter_with_discount",
        initial=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aggregate_limits = self.get_aggregate_limits()
        self.form.fields["max_price"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "max_price_input",
                "min": self._aggregate_limits["min_price"],
                "max": self._aggregate_limits["max_price"],
                "value": self._aggregate_limits["max_price"],
            }
        )
        self.form.fields["min_price"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "min_price_input",
                "min": self._aggregate_limits["min_price"],
                "max": self._aggregate_limits["max_price"],
                "value": self._aggregate_limits["min_price"],
            }
        )

    class Meta:
        fields = [
            "price",
            "discount",
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

    def filter_with_discount(self, queryset, name, value):
        return queryset.filter(discount__gt=0) if value else queryset.filter(discount=0)
