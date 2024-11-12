from django.contrib import admin

from .models import RobotsTxt, SitemapPage


class RobotsTxtAdmin(admin.ModelAdmin):
    list_display = ("id", "content")
    search_fields = ("content",)


class SitemapPageAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "last_modified", "changefreq", "priority")
    search_fields = ("name", "url")


admin.site.register(RobotsTxt, RobotsTxtAdmin)
admin.site.register(SitemapPage, SitemapPageAdmin)
