# Generated by Django 5.1.4 on 2025-02-23 17:36

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0064_alter_bouquet_tax_percent_alter_product_tax_percent"),
    ]

    operations = [
        migrations.AddField(
            model_name="bouquet",
            name="description_gr",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="name_gr",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="slug_gr",
            field=models.SlugField(
                max_length=80, null=True, unique=True, verbose_name="Название в ссылке"
            ),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="specs_gr",
            field=tinymce.models.HTMLField(null=True, verbose_name="Характеристики"),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="catalog_page_meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги на странице категории со списком подкатегорий",
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="description_gr",
            field=tinymce.models.HTMLField(
                null=True, verbose_name="Описание на странице категории"
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="name_gr",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="slug_gr",
            field=models.SlugField(
                max_length=80, null=True, unique=True, verbose_name="Название в ссылке"
            ),
        ),
        migrations.AddField(
            model_name="bouquetimage",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="bouquetsizeimage",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="bouquetslistpagemodel",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetsubcategory",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="bouquetsubcategory",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetsubcategory",
            name="name_gr",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="bouquetsubcategory",
            name="slug_gr",
            field=models.SlugField(
                max_length=80, null=True, unique=True, verbose_name="Название в ссылке"
            ),
        ),
        migrations.AddField(
            model_name="catalogpagemodel",
            name="description_gr",
            field=tinymce.models.HTMLField(
                null=True, verbose_name="Описание на странице 'Каталог'"
            ),
        ),
        migrations.AddField(
            model_name="catalogpagemodel",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="color",
            name="name_gr",
            field=models.CharField(
                max_length=15, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="flower",
            name="name_gr",
            field=models.CharField(
                max_length=30, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="description_gr",
            field=tinymce.models.HTMLField(null=True, verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="product",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="name_gr",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="slug_gr",
            field=models.SlugField(
                max_length=80, null=True, unique=True, verbose_name="Название в ссылке"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="specs_gr",
            field=tinymce.models.HTMLField(null=True, verbose_name="Характеристики"),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="catalog_page_meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги на странице категории со списком подкатегорий",
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="description_gr",
            field=tinymce.models.HTMLField(
                null=True, verbose_name="Описание на странице категории"
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="name_gr",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="slug_gr",
            field=models.SlugField(
                max_length=80, null=True, unique=True, verbose_name="Название в ссылке"
            ),
        ),
        migrations.AddField(
            model_name="productimage",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="productslistpagemodel",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productsubcategory",
            name="image_alt_gr",
            field=models.CharField(
                max_length=200, null=True, verbose_name="Описание картинки"
            ),
        ),
        migrations.AddField(
            model_name="productsubcategory",
            name="meta_tags_gr",
            field=models.TextField(
                default='<title> | BlumenHorizon</title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productsubcategory",
            name="name_gr",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="Название"
            ),
        ),
        migrations.AddField(
            model_name="productsubcategory",
            name="slug_gr",
            field=models.SlugField(
                max_length=80, null=True, unique=True, verbose_name="Название в ссылке"
            ),
        ),
    ]
