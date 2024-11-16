from django.contrib import admin

from .models import IndividualOrder, MainPageMetaTags, MainPageSliderImages, SeoBlock


@admin.register(MainPageSliderImages)
class MainPageSliderAdmin(admin.ModelAdmin):
    fields = ["image", "image_alt", "is_active"]
    list_display = ["image", "image_alt", "is_active"]


@admin.register(SeoBlock)
class SeoBlockAdmin(admin.ModelAdmin):
    fields = ["image", "image_alt"]
    list_display = ["image", "image_alt"]


@admin.register(IndividualOrder)
class IndividualOrderAdmin(admin.ModelAdmin):
    fields = ["first_name", "contact_method", "recall_me", "user"]
    list_display = ["user", "first_name", "contact_method", "recall_me"]


@admin.register(MainPageMetaTags)
class MainPageMetaTagsAdmin(admin.ModelAdmin):
    fields = ["meta_tags"]
    list_display = ["id"]
