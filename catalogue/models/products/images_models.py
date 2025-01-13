from django.db import models

from core.services.utils.urls import build_absolute_url

from .product import Product


class ProductImage(models.Model):
    item = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    image = models.ImageField(
        upload_to="products/%Y-%m-%d/",
        default="defaults/no-image.webp",
        verbose_name="Изображение продукта",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

    def __str__(self):
        return f"{self.item.name} - Image"

    @property
    def absolute_url(self):
        return build_absolute_url(
            relative_url=self.image.url,
            is_media=True,
        )
