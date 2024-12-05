# Generated by Django 5.1.3 on 2024-12-05 15:11

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0038_aboutuspagemodel_json_ld_de_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="description_ua",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="image_alt_ua",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="image_ua",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                null=True,
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="json_ld_ua",
            field=models.TextField(
                default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                max_length=4000,
                null=True,
                verbose_name="JSON-LD",
            ),
        ),
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="meta_tags_ua",
            field=models.TextField(
                default="<title>Blumen Horizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="description_ua",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="image_alt_ua",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="image_ua",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                null=True,
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="json_ld_ua",
            field=models.TextField(
                default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                max_length=4000,
                null=True,
                verbose_name="JSON-LD",
            ),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="meta_tags_ua",
            field=models.TextField(
                default="<title>Blumen Horizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="description_ua",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="image_alt_ua",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="image_ua",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                null=True,
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="json_ld_ua",
            field=models.TextField(
                default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                max_length=4000,
                null=True,
                verbose_name="JSON-LD",
            ),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="meta_tags_ua",
            field=models.TextField(
                default="<title>Blumen Horizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="description_ua",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="image_alt_ua",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="image_ua",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                null=True,
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="meta_tags_ua",
            field=models.TextField(
                default="<title>Blumen Horizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="mainpagemodel",
            name="description_ua",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="mainpagemodel",
            name="json_ld_description_ua",
            field=models.CharField(
                default="Blumen Horizon интернет-магазин цветов и подарков в Берлине",
                max_length=500,
                null=True,
                verbose_name="Description в JSON LD для OnlineStore",
            ),
        ),
        migrations.AddField(
            model_name="mainpagemodel",
            name="meta_tags_ua",
            field=models.TextField(
                default="<title>Blumen Horizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="mainpageseoblock",
            name="image_alt_ua",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="mainpageseoblock",
            name="image_ua",
            field=models.ImageField(
                help_text="1000px/450px",
                null=True,
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AddField(
            model_name="mainpagesliderimages",
            name="image_alt_ua",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="mainpagesliderimages",
            name="image_ua",
            field=models.ImageField(
                help_text="1000px/450px",
                null=True,
                upload_to="mainpage-slider/",
                verbose_name="Фото на главном слайде",
            ),
        ),
    ]
