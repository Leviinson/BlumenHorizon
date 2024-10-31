from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms.user_form import UserForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        "email",
        "phonenumber",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "date_joined")
    search_fields = ("email", "phonenumber", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phonenumber",
                    "email",
                    "is_active",
                ),
                "classes": [
                    "wide",
                ],
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": [
                    "wide",
                ],
            },
        ),
    )

    search_help_text = (
        "Поиск по адресу электронной почты, номеру телефона, имени или фамилии."
    )
