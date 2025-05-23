# Generated by Django 5.1.3 on 2024-12-08 21:36

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "mainpage",
            "0040_rename_description_ua_aboutuspagemodel_description_uk_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="AGBPageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                ("description", tinymce.models.HTMLField(verbose_name="Описание")),
                (
                    "description_de",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_en",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_ru",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_uk",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "meta_tags",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_de",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_en",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_ru",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_uk",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "json_ld",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_de",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_en",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_ru",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_uk",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
            ],
            options={
                "verbose_name": "Условия и положения",
                "verbose_name_plural": "Условия и положения",
            },
        ),
        migrations.CreateModel(
            name="ImpressumPageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                ("description", tinymce.models.HTMLField(verbose_name="Описание")),
                (
                    "description_de",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_en",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_ru",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_uk",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "meta_tags",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_de",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_en",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_ru",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_uk",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "json_ld",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_de",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_en",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_ru",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_uk",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
            ],
            options={
                "verbose_name": "Контактная информация",
                "verbose_name_plural": "Контактная информация",
            },
        ),
        migrations.CreateModel(
            name="PrivacyAndPolicyPageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                ("description", tinymce.models.HTMLField(verbose_name="Описание")),
                (
                    "description_de",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_en",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_ru",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_uk",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "meta_tags",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_de",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_en",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_ru",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_uk",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "json_ld",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_de",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_en",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_ru",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_uk",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
            ],
            options={
                "verbose_name": "Условия конфиденциальности и безопасности данных",
                "verbose_name_plural": "Условия конфиденциальности и безопасности данных",
            },
        ),
        migrations.CreateModel(
            name="ReturnPolicyPageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                ("description", tinymce.models.HTMLField(verbose_name="Описание")),
                (
                    "description_de",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_en",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_ru",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "description_uk",
                    tinymce.models.HTMLField(null=True, verbose_name="Описание"),
                ),
                (
                    "meta_tags",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_de",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_en",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_ru",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "meta_tags_uk",
                    models.TextField(
                        default="<title>Blumen Horizon | </title>",
                        max_length=1000,
                        null=True,
                        verbose_name="Мета-теги",
                    ),
                ),
                (
                    "json_ld",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_de",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_en",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_ru",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
                (
                    "json_ld_uk",
                    models.TextField(
                        default='<script type="application/ld+json">\n        {\n            "@context": "https://schema.org",\n            "@type": "WebPage"\n        }\n</script>',
                        max_length=4000,
                        null=True,
                        verbose_name="JSON-LD",
                    ),
                ),
            ],
            options={
                "verbose_name": "Условия возврата",
                "verbose_name_plural": "Условия возврата",
            },
        ),
    ]
