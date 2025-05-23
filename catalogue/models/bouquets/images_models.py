from django.db import models

from core.services.utils.urls import build_absolute_url

from .bouquet import Bouquet, BouquetSize


class BouquetImage(models.Model):
    item = models.ForeignKey(
        Bouquet,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Букет",
    )
    image = models.ImageField(
        upload_to="bouquets/%Y-%m-%d/",
        verbose_name="Изображение букета",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Изображение букета"
        verbose_name_plural = "Изображения букетов"

    def __str__(self):
        return f"{self.item.name} - Image"

    @property
    def absolute_url(self):
        return build_absolute_url(
            relative_url=self.image.url,
        )


class BouquetSizeImage(models.Model):
    bouquet_size = models.ForeignKey(
        BouquetSize,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Размер букета",
    )
    image = models.ImageField(
        upload_to="bouquets/sizes/%Y-%m-%d/",
        verbose_name="Изображение размера букета",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Изображение размера букета"
        verbose_name_plural = "Изображения размеров букетов"

    @property
    def absolute_url(self):
        return build_absolute_url(
            relative_url=self.image.url,
        )
