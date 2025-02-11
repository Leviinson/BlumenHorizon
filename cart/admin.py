from django.contrib import admin

from .models import (
    BankAccount,
    Bill,
    Florist,
    Order,
    OrderBouquets,
    OrderProducts,
    RefundReceipt,
)


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
        "brutto",
        "netto",
        "tax",
        "created_at",
        "is_paid"
    )
    search_fields = ("number", "florist__title")
    list_filter = ("florist", "account_paid_funds", "created_at")
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "number",
                    "florist",
                    "account_paid_funds",
                    "refund_receipt",
                    "is_paid",
                ),
            },
        ),
        (
            "Цены",
            {
                "fields": (
                    "brutto",
                    "netto",
                    "tax",
                ),
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


@admin.register(RefundReceipt)
class RefundReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "issue_date",
        "receipt_date",
        "refund_amount",
        "account_received_funds",
        "image_display",
    )

    list_filter = (
        "account_received_funds__title",
        "issue_date",
        "receipt_date",
    )

    search_fields = (
        "account_received_funds__title",
        "account_received_funds__number",
        "refund_amount",
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "image",
                    "issue_date",
                    "receipt_date",
                    "refund_amount",
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("account_received_funds",),
            },
        ),
    )

    def image_display(self, obj):
        if obj.image:
            return f"\u2714 {obj.image.name}"
        return "\u2718 Нет файла"

    image_display.short_description = "Файл подтверждения"
    ordering = ("-receipt_date",)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner_name",
        "number",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "owner_name",
        "number",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "owner_name",
                    "number",
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")


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
                    "grand_total",
                    "sub_total",
                    "tax",
                    "stripe_taxes",
                ),
            },
        ),
        (
            "Данные отправителя",
            {
                "fields": (
                    "address_form",
                    "name",
                    "email",
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
                    "clarify_address",
                    "country",
                    "city",
                    "postal_code",
                    "street",
                    "building",
                    "flat",
                    "is_recipient",
                    "is_surprise",
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
