from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "date_joined")
    search_fields = ("email", "phone_number", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (
            "Личная информация",
            {
                "fields": ("first_name", "last_name", "phone_number", "email"),
                "classes": [
                    "collapse in",
                ],
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )

    search_help_text = _(
        "Поиск по адресу электронной почты, номеру телефона, имени или фамилии."
    )
