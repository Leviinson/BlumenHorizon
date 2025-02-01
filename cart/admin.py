from django.contrib import admin

from .models import Order, OrderBouquets, OrderProducts


class OrderProductsStackedInline(admin.StackedInline):
    model = OrderProducts
    extra = 0


class OrderBouquetsStackedInline(admin.StackedInline):
    model = OrderBouquets
    extra = 0


@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    inlines = (
        OrderProductsStackedInline,
        OrderBouquetsStackedInline,
    )
    fields = (
        "user",
        "status",
        "sub_total",
        "tax",
        "tax_percent",
        "grand_total",
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
        "code",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "code",
    )
    list_display = (
        "grand_total",
        "delivery_date",
        "delivery_time",
        "street",
        "building",
        "flat",
        "recipient_name",
        "recipient_phonenumber",
        "code",
        "user",
    )
    search_fields = (
        "code",
        "recipient_phonenumber",
        "email",
    )
