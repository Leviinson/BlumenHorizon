# Generated by Django 5.1.2 on 2024-11-07 23:07

from django.db import migrations, models

import catalogue.models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0007_bouquet_sku_product_sku"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bouquet",
            name="sku",
            field=models.CharField(
                default=catalogue.models.generate_sku,
                max_length=6,
                null=True,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="sku",
            field=models.CharField(
                default=catalogue.models.generate_sku,
                max_length=6,
                null=True,
                unique=True,
            ),
        ),
    ]
