from django.contrib import admin

from .models import MainPageSliderImages


class SliderImagesInline(admin.TabularInline):
    model = MainPageSliderImages
    extra = 1
    max_num = 3
    fields = ["is_active"]


@admin.register(MainPageSliderImages)
class MainPageSliderAdmin(admin.ModelAdmin):
    fields = ["image", "is_active"]
