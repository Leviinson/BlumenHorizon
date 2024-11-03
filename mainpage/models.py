from django.db import models


# Create your models here.
class MainPageSliderImages(models.Model):
    image = models.ImageField(verbose_name="Фото на главном слайде")
    is_active = models.BooleanField(default=False, verbose_name="Активное?")

    class Meta:
        verbose_name = "Фото слайдера главной страницы"
        verbose_name_plural = "Фотографии слайдера главной страницы"
