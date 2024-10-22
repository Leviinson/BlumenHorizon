from django.contrib import admin

from .models import ExtendedSite


@admin.register(ExtendedSite)
class ExtendedSiteAdmin(admin.ModelAdmin):
    list_display = ('site', 'currency_code', 'currency_symbol')
    search_fields = ('site__domain', 'currency_code', 'currency_symbol')