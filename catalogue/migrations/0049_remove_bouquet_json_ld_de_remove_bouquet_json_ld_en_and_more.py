# Generated by Django 5.1.3 on 2024-11-27 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0048_alter_bouquetslistpagemodel_json_ld_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bouquet",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="bouquet",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="bouquet",
            name="json_ld_ru",
        ),
        migrations.RemoveField(
            model_name="bouquetcategory",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="bouquetcategory",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="bouquetcategory",
            name="json_ld_ru",
        ),
        migrations.RemoveField(
            model_name="bouquetsubcategory",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="bouquetsubcategory",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="bouquetsubcategory",
            name="json_ld_ru",
        ),
        migrations.RemoveField(
            model_name="catalogpagemodel",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="catalogpagemodel",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="catalogpagemodel",
            name="json_ld_ru",
        ),
        migrations.RemoveField(
            model_name="product",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="product",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="product",
            name="json_ld_ru",
        ),
        migrations.RemoveField(
            model_name="productcategory",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="productcategory",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="productcategory",
            name="json_ld_ru",
        ),
        migrations.RemoveField(
            model_name="productsubcategory",
            name="json_ld_de",
        ),
        migrations.RemoveField(
            model_name="productsubcategory",
            name="json_ld_en",
        ),
        migrations.RemoveField(
            model_name="productsubcategory",
            name="json_ld_ru",
        ),
    ]
