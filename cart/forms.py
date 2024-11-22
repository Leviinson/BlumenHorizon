from decimal import Decimal

from django import forms
from django.db import transaction

from accounts.models import User
from catalogue.models import Bouquet, Product
from core.services.decorators.db.db_queries import inspect_db_queries

from .cart import BouquetCart, ProductCart
from .models import Order, OrderBouquets, OrderProducts


class CartForm(forms.Form):
    product_slug = forms.SlugField()


class OrderForm(forms.ModelForm):
    country = forms.CharField(required=False, widget=forms.TextInput())
    city = forms.CharField(required=False, widget=forms.TextInput())
    postal_code = forms.CharField(required=False, widget=forms.TextInput())
    street = forms.CharField(required=False, widget=forms.TextInput())
    building = forms.CharField(required=False, widget=forms.TextInput())
    flat = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = Order
        fields = [
            "clarify_address",
            "country",
            "city",
            "email",
            "address_form",
            "name",
            "postal_code",
            "street",
            "building",
            "flat",
            "recipient_address_form",
            "recipient_name",
            "recipient_phonenumber",
            "is_recipient",
            "is_surprise",
        ]

    def save(
        self,
        products_cart: ProductCart,
        bouquets_cart: BouquetCart,
        tax_percent: int,
        commit=True,
        user: User = None,
    ) -> Order:
        order: Order = super().save(commit=False)
        if user and user.is_authenticated:
            order.user = user
        with transaction.atomic():
            sub_total = products_cart.total + bouquets_cart.total
            order.tax_percent = tax_percent
            order.tax = tax = sub_total * Decimal(tax_percent/100)
            order.sub_total = sub_total
            order.grand_total = sub_total + tax
            order.save()
            if products := products_cart.products:
                OrderProducts.objects.bulk_create(
                    [
                        OrderProducts(order=order, product=product, quantity=products_cart.get_quantity(product))
                        for product in products
                    ]
                )
            if bouquets := bouquets_cart.products:
                OrderBouquets.objects.bulk_create(
                    [
                        OrderBouquets(order=order, product=bouquet, quantity=bouquets_cart.get_quantity(bouquet))
                        for bouquet in bouquets
                    ]
                )
        return order
