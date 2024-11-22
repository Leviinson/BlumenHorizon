from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel


class MainPageModel(models.Model):
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="<title>BlumenHorizon | </title>",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=1000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
        </script>""",
    )
    description = HTMLField(
        verbose_name=_("Описание"),
    )

    class Meta:
        verbose_name = "Мета-тег и разметка главной страницы"
        verbose_name_plural = "Мета-теги и разметка главной страницы"

    def __str__(self):
        return "Мета-теги главной страницы"


class MainPageSliderImages(models.Model):
    image = models.ImageField(
        upload_to="mainpage-slider/",
        verbose_name="Фото на главном слайде",
        help_text="1000px/450px",
    )
    is_active = models.BooleanField(default=False, verbose_name="Активное?")
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = "Фото слайдера главной страницы"
        verbose_name_plural = "Фотографии слайдера главной страницы"

    def __str__(self):
        return f"{self.image} - {"Активно" if self.is_active else "Неактивно"}"


class IndividualOrder(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="individual_orders",
        verbose_name="Связанный аккаунт",
        null=True,
        blank=False,
    )
    first_name = models.CharField(max_length=40, verbose_name="Имя")
    contact_method = models.TextField(
        max_length=100,
        verbose_name=_("Способ связи с клиентом"),
    )
    recall_me = models.BooleanField(
        verbose_name="Разрешил ли клиент звонить ему", default=False
    )

    class Meta:
        verbose_name = "Индивидуальный заказ"
        verbose_name_plural = "Индивидуальные заказы"

    def __str__(self):
        return f"{self.first_name}"


class MainPageSeoBlock(TimeStampAdbstractModel, models.Model):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="seoblock/",
        help_text="1000px/450px",
    )
    image_alt = models.CharField(max_length=100, verbose_name="Описание картинки")

    class Meta:
        verbose_name = "СЕО Блок"
        verbose_name_plural = "СЕО Блоки"

    def __str__(self):
        return f"{self.image} ...... {self.alt}"


class FAQPageModel(TimeStampAdbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="seoblock/",
        default="defaults/no-image.webp",
        help_text="1000px/450px",
    )
    image_alt = models.CharField(max_length=100, verbose_name="Описание картинки")
    description = HTMLField(
        verbose_name=_("Описание"),
    )
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="<title>BlumenHorizon | </title>",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=1000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
</script>""",
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Частозадаваемые вопросы"
        verbose_name_plural = verbose_name


class AboutUsPageModel(TimeStampAdbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="seoblock/",
        default="defaults/no-image.webp",
        help_text="1000px/450px",
    )
    image_alt = models.CharField(max_length=100, verbose_name="Описание картинки")
    description = HTMLField(
        verbose_name=_("Описание"),
    )
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="<title>BlumenHorizon | </title>",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=1000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
</script>""",
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = verbose_name


class DeliveryPageModel(TimeStampAdbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="seoblock/",
        default="defaults/no-image.webp",
        help_text="1000px/450px",
    )
    image_alt = models.CharField(max_length=100, verbose_name="Описание картинки")
    description = HTMLField(
        verbose_name=_("Описание"),
    )
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="<title>BlumenHorizon | </title>",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=1000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
</script>""",
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = verbose_name


class ContactsPageModel(TimeStampAdbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="seoblock/",
        default="defaults/no-image.webp",
        help_text="1000px/450px",
    )
    image_alt = models.CharField(max_length=100, verbose_name="Описание картинки")
    description = HTMLField(
        verbose_name=_("Описание"),
    )
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="<title>BlumenHorizon | </title>",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=1000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
</script>""",
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = verbose_name
