import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View

from cart.cart import BouquetsCart, ProductsCart

from .models import PaymentMethod

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        # Получаем активные методы оплаты
        active_payment_methods = PaymentMethod.objects.filter(is_active=True)
        payment_method_types = [method.stripe_code for method in active_payment_methods]

        # Получаем продукты из корзин
        cart_products = ProductsCart(
            request.session, session_key="products_cart"
        ).products
        bouquets_cart = BouquetsCart(
            request.session, session_key="bouquets_cart"
        ).products

        # Подготавливаем line_items для Stripe
        line_items = []
        for product in cart_products + bouquets_cart:
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product.name,
                        },
                        "unit_amount": int(product.price * 100),
                    },
                    "quantity": 1,
                }
            )

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=payment_method_types,
                line_items=line_items,
                mode="payment",
                success_url=request.build_absolute_uri("/success/"),
                cancel_url=request.build_absolute_uri("/cancel/"),
            )
            return redirect(session.url)
        except Exception as e:
            print(f"Error creating checkout session: {e}")
            return redirect("/error/")
