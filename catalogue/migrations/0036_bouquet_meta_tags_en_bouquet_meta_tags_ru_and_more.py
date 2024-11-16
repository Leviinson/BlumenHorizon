# Generated by Django 5.1.2 on 2024-11-16 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0035_alter_bouquet_meta_tags_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bouquet",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetslistpagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetslistpagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetsubcategory",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="bouquetsubcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="catalogpagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="catalogpagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="categorypagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="categorypagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productslistpagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productslistpagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productsubcategory",
            name="meta_tags_en",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AddField(
            model_name="productsubcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
    ]
