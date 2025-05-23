# Generated by Django 5.1.2 on 2024-11-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0003_productcategory_rename_category_bouquetcategory_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bouquet",
            name="amount_of_orders",
            field=models.IntegerField(
                default=0, editable=False, verbose_name="Количество заказов у продукта"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bouquet",
            name="amount_of_savings",
            field=models.IntegerField(
                default=0,
                editable=False,
                verbose_name="Количество добавлений в карзину",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="amount_of_orders",
            field=models.IntegerField(
                default=0, editable=False, verbose_name="Количество заказов у продукта"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="amount_of_savings",
            field=models.IntegerField(
                default=0,
                editable=False,
                verbose_name="Количество добавлений в карзину",
            ),
            preserve_default=False,
        ),
    ]
