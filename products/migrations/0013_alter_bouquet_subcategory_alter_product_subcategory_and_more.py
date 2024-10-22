# Generated by Django 5.1.2 on 2024-10-22 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0012_bouquet_discount_product_discount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bouquet",
            name="subcategory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="products.subcategory",
                verbose_name="Подкатегория",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="subcategory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="products.subcategory",
                verbose_name="Подкатегория",
            ),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcategories",
                to="products.category",
                verbose_name="Категория",
            ),
        ),
    ]
