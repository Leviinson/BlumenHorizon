# Generated by Django 5.1.4 on 2025-02-24 13:38

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0048_alter_aboutuspagemodel_meta_tags_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="image_alt_el",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="aboutuspagemodel",
            name="image_el",
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
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="agbpagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="agbpagemodel",
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="image_alt_el",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="contactspagemodel",
            name="image_el",
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
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="image_alt_el",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="deliverypagemodel",
            name="image_el",
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
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="image_alt_el",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="faqpagemodel",
            name="image_el",
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
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="impressumpagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="impressumpagemodel",
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="mainpagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="mainpagemodel",
            name="json_ld_description_el",
            field=models.CharField(
                default="Blumen Horizon интернет-магазин цветов и подарков в Берлине",
                max_length=500,
                null=True,
                verbose_name="Description в JSON LD для OnlineStore",
            ),
        ),
        migrations.AddField(
            model_name="mainpagemodel",
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="mainpageseoblock",
            name="image_alt_el",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="mainpageseoblock",
            name="image_el",
            field=models.ImageField(
                help_text="1000px/450px",
                null=True,
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AddField(
            model_name="mainpagesliderimages",
            name="image_alt_el",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="mainpagesliderimages",
            name="image_el",
            field=models.ImageField(
                help_text="1000px/450px",
                null=True,
                upload_to="mainpage-slider/",
                verbose_name="Фото на главном слайде",
            ),
        ),
        migrations.AddField(
            model_name="privacyandpolicypagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="privacyandpolicypagemodel",
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="returnpolicypagemodel",
            name="description_el",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="returnpolicypagemodel",
            name="meta_tags_el",
            field=models.TextField(
                default="<title> | BlumenHorizon</title>",
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
    ]
