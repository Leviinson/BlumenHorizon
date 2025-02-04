from typing import Any, Optional

from django import forms
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from accounts.models import User

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
            "is_agreement_accepted",
        ]

    def save(
        self,
        products_cart: ProductCart,
        bouquets_cart: BouquetCart,
        session_key: Any,
        language_code: str,
        user: User | AnonymousUser,
        commit=True,
    ) -> Order:
        """
        Сохраняет заказ с расчётами налогов, сумм и связывает продукты и букеты с заказом.

        Параметры:
        products_cart (ProductCart): Корзина с продуктами пользователя.
        bouquets_cart (BouquetCart): Корзина с букетами пользователя.
        session_key (Any): Ключ сессии пользователя.
        language_code (str): Код языка для локализации заказа.
        commit (bool): Флаг для немедленного сохранения заказа в базу.
        user (User, optional): Пользователь, сделавший заказ (если аутентифицирован).

        Возвращает:
        Order: Сохранённый объект заказа.
        """
        order = self._initialize_order(session_key, user, language_code)

        with transaction.atomic():
            self._calculate_and_save_totals(order, products_cart, bouquets_cart)
            self._save_order_products(order, products_cart)
            self._save_order_bouquets(order, bouquets_cart)

        return order

    def _initialize_order(
        self, session_key: Any, user: Optional[User], language_code: str
    ) -> Order:
        """
        Инициализирует заказ с необходимыми аттрибутами, без его сохранения.

        Параметры:
        session_key (Any): Ключ сессии пользователя.
        user (Optional[User]): Пользователь, если аутентифицирован.
        language_code (str): Код языка для локализации.

        Возвращает:
        Order: Новый объект заказа.
        """
        order = super().save(commit=False)
        order.session_key = session_key
        if user and user.is_authenticated:
            order.user = user
        order.language_code = language_code
        return order

    def _calculate_and_save_totals(
        self,
        order: Order,
        products_cart: ProductCart,
        bouquets_cart: BouquetCart,
    ):
        """
        Рассчитывает налог, сумму без налога, общую сумму заказа,
        присваивает значения заказу и сохраняет его.

        Параметры:
        order (Order): Объект заказа, в котором будут сохранены вычисленные значения.
        products_cart (ProductCart): Корзина с продуктами.
        bouquets_cart (BouquetCart): Корзина с букетами.
        """
        grand_total = products_cart.total + bouquets_cart.total
        tax = products_cart.total_tax_amount + bouquets_cart.total_tax_amount
        sub_total = grand_total - tax

        order.tax = tax
        order.grand_total = grand_total
        order.sub_total = sub_total
        order.save()

    def _save_order_products(self, order: Order, products_cart: ProductCart):
        """
        Сохраняет товары из корзины продуктов в таблицу OrderProducts.

        Параметры:
        order (Order): Объект заказа.
        products_cart (ProductCart): Корзина с продуктами.
        """
        if products := products_cart.products:
            OrderProducts.objects.bulk_create(
                [
                    OrderProducts(
                        order=order,
                        product=product,
                        base_price=product.price,
                        discount=product.discount,
                        discount_price=product.discount_price,
                        tax_price=product.tax_price,
                        tax_price_discounted=product.tax_price_discounted,
                        taxes=product.taxes
                        * products_cart.get_product_quantity(product),
                        quantity=products_cart.get_product_quantity(product),
                    )
                    for product in products
                ]
            )

    def _save_order_bouquets(self, order: Order, bouquets_cart: BouquetCart):
        """
        Сохраняет товары из корзины букетов в таблицу OrderBouquets.

        Параметры:
        order (Order): Объект заказа.
        bouquets_cart (BouquetCart): Корзина с букетами.
        """
        if bouquets := bouquets_cart.products:
            OrderBouquets.objects.bulk_create(
                [
                    OrderBouquets(
                        order=order,
                        product=bouquet,
                        base_price=bouquet.price,
                        discount=bouquet.discount,
                        discount_price=bouquet.discount_price,
                        tax_price=bouquet.tax_price,
                        tax_price_discounted=bouquet.tax_price_discounted,
                        taxes=bouquet.taxes
                        * bouquets_cart.get_product_quantity(bouquet),
                        quantity=bouquets_cart.get_product_quantity(bouquet),
                    )
                    for bouquet in bouquets
                ]
            )

    def clean_is_agreement_accepted(self):
        agreement = self.cleaned_data["is_agreement_accepted"]
        if not agreement:
            raise forms.ValidationError(
                _("Вы должны согласиться с данными правилами."),
            )
        return agreement
