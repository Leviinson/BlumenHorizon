from django.contrib import admin

from .models import Bill, Florist, Order, OrderBouquets, OrderProducts


class BillInline(admin.StackedInline):
    model = Bill
    extra = 0
    show_change_link = True


class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    show_change_link = True


@admin.register(Florist)
class FloristAdmin(admin.ModelAdmin):
    list_display = ("title", "contact", "address", "vat_id")
    search_fields = ("title", "contact", "vat_id")
    list_filter = ("vat_id",)
    fieldsets = (
        ("Основная информация", {"fields": ("title", "contact", "address")}),
        (
            "Дополнительно",
            {
                "fields": ("vat_id", "description"),
            },
        ),
    )
    ordering = ("title",)
    inlines = [
        BillInline,
    ]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "florist",
        "order",
        "brutto",
        "netto",
        "tax",
        "created_at",
    )
    search_fields = ("number", "florist__title")
    list_filter = ("florist", "created_at")
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("number", "florist", "order"),
            },
        ),
        (
            "Цены",
            {
                "fields": ("brutto", "netto", "tax"),
            },
        ),
        (
            "Изображение",
            {
                "fields": ("image",),
            },
        ),
    )
    ordering = ("-created_at",)
    autocomplete_fields = ("florist",)


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

    fieldsets = (
        (
            "Общая информация",
            {
                "fields": (
                    "user",
                    "status",
                    "bill",
                    "code",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            "Стоимость",
            {
                "fields": (
                    "sub_total",
                    "tax",
                    "grand_total",
                ),
            },
        ),
        (
            "Данные отправителя",
            {
                "fields": (
                    "name",
                    "email",
                    "clarify_address",
                    "address_form",
                    "country",
                    "city",
                    "postal_code",
                    "street",
                    "building",
                    "flat",
                ),
            },
        ),
        (
            "Данные получателя",
            {
                "fields": (
                    "recipient_address_form",
                    "recipient_name",
                    "recipient_phonenumber",
                    "is_recipient",
                    "is_surprise",
                ),
            },
        ),
        (
            "Доставка",
            {
                "fields": (
                    "delivery_date",
                    "delivery_time",
                    "instructions",
                ),
            },
        ),
        (
            "Открытка",
            {
                "fields": ("message_card",),
            },
        ),
        (
            "Согласия",
            {
                "fields": ("is_agreement_accepted",),
            },
        ),
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
        "recipient_name",
        "recipient_phonenumber",
        "street",
        "building",
        "flat",
        "code",
        "user",
    )

    search_fields = (
        "code",
        "recipient_phonenumber",
        "email",
    )

    ordering = ("-created_at",)
