from django.contrib import admin

from .models import Order, OrderBouquets, OrderProducts

class OrderProductsTabularInline(admin.TabularInline):
    model = OrderProducts
    extra = 1

class OrderBouquetsTabularInline(admin.TabularInline):
    model = OrderBouquets
    extra = 1

@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    inlines = (
        OrderProductsTabularInline,
        OrderBouquetsTabularInline
    )
    fields = (
        "user",
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
        "code",
        "user",
        "street",
        "recipient_name",
        "recipient_phonenumber",
        "building",
        "flat",
    )
