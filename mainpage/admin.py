from django.contrib import admin

from .models import IndividualOrder, MainPageSliderImages, SeoBlock


class SliderImagesInline(admin.TabularInline):
    model = MainPageSliderImages
    extra = 1
    max_num = 3
    fields = ["is_active"]


@admin.register(MainPageSliderImages)
class MainPageSliderAdmin(admin.ModelAdmin):
    fields = ["image", "is_active"]
    list_display = ["image", "is_active"]


@admin.register(SeoBlock)
class SeoBlockAdmin(admin.ModelAdmin):
    fields = ["image", "alt"]
    list_display = ["image", "alt"]


@admin.register(IndividualOrder)
class IndividualOrderAdmin(admin.ModelAdmin):
    fields = ["first_name", "contact_method", "recall_me", "user"]
    list_display = ["user", "first_name", "contact_method", "recall_me"]
