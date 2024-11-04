from django.contrib import admin

from .models import ExtendedSite, Social


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = (
        "absolute_url",
        "background_hex_code",
        "bootstrap_icon",
        "extended_site",
    )
    search_fields = ("absolute_url", "bootstrap_icon", "extended_site__site__domain")


class SocialInline(admin.TabularInline):
    model = Social
    extra = 1
    max_num = 3
    verbose_name = "Соц. сеть"
    verbose_name_plural = "Социальные сети"


@admin.register(ExtendedSite)
class ExtendedSiteAdmin(admin.ModelAdmin):
    list_display = ("site", "currency_code", "currency_symbol", "country", "city")
    search_fields = (
        "site__domain",
        "currency_code",
        "currency_symbol",
        "country",
        "city",
    )
    inlines = [SocialInline]
