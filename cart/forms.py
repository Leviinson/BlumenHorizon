from django import forms
from django.db import transaction
from django.db.models.manager import BaseManager

from accounts.models import User
from catalogue.models import Bouquet, Product

from .models import Order, OrderBouquets, OrderProducts


class CartForm(forms.Form):
    product_slug = forms.SlugField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "clarify_address",
            "country",
            "city",
            "email",
            "postal_code",
            "street",
            "building",
            "flat",
            "recipient_name",
            "recipient_phonenumber",
            "is_recipient",
            "is_surprise",
        ]

    def save(
        self,
        products: BaseManager[Product],
        bouquets: BaseManager[Bouquet],
        commit=True,
        user: User = None,
    ):
        order: Order = super().save(commit=False)
        if user and user.is_authenticated:
            order.user = user
        with transaction.atomic():
            order.save()
            if products:
                OrderProducts.objects.bulk_create(
                    [
                        OrderProducts(order=order, product=product)
                        for product in products
                    ]
                )
            if bouquets:
                OrderBouquets.objects.bulk_create(
                    [
                        OrderBouquets(order=order, product=bouquet)
                        for bouquet in bouquets
                    ]
                )
        return order
