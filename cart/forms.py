from decimal import Decimal

from django import forms
from django.db import transaction

from accounts.models import User
from catalogue.models import Bouquet, Product

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
    delivery_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "id": "delivery-date",
            }
        ),
    )
    delivery_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "id": "delivery-time",
            }
        ),
    )
    message_card = forms.CharField(required=False, widget=forms.Textarea())
    instructions = forms.CharField(required=False, widget=forms.Textarea())

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
            "delivery_date",
            "delivery_time",
            "message_card",
            "instructions",
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
            grand_total = products_cart.total + bouquets_cart.total
            sub_total = sub_total = grand_total / Decimal(1 + tax_percent / 100)
            order.tax = grand_total - sub_total
            order.tax_percent = tax_percent
            order.grand_total = grand_total
            order.sub_total = sub_total
            order.save()
            if products := products_cart.products:
                products: list[Product] = products
                OrderProducts.objects.bulk_create(
                    [
                        OrderProducts(
                            order=order,
                            product=product,
                            product_price=product.price,
                            product_discount=(
                                product.discount if product.has_discount else 0
                            ),
                            product_discount_price=product.discount_price,
                            product_tax_price=product.tax_price,
                            product_tax_price_discounted=product.tax_price_discounted,
                            quantity=products_cart.get_quantity(product),
                        )
                        for product in products
                    ]
                )
            if bouquets := bouquets_cart.products:
                bouquets: list[Bouquet] = bouquets
                OrderBouquets.objects.bulk_create(
                    [
                        OrderBouquets(
                            order=order,
                            product=bouquet,
                            product_price=bouquet.price,
                            product_discount=(
                                bouquet.discount if bouquet.has_discount else 0
                            ),
                            product_discount_price=bouquet.discount_price,
                            product_tax_price=bouquet.tax_price,
                            product_tax_price_discounted=bouquet.tax_price_discounted,
                            quantity=bouquets_cart.get_quantity(bouquet),
                        )
                        for bouquet in bouquets
                    ]
                )
        return order
