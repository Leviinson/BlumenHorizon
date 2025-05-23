# Generated by Django 5.1.2 on 2024-11-07 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0006_alter_bouquet_discount_alter_product_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="bouquet",
            name="sku",
            field=models.CharField(default=None, max_length=6, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="product",
            name="sku",
            field=models.CharField(default=None, max_length=6, null=True, unique=True),
        ),
    ]
