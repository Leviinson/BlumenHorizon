# Generated by Django 5.1.2 on 2024-11-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalogue",
            "0004_bouquet_amount_of_orders_bouquet_amount_of_savings_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="bouquet",
            name="amount_of_orders",
            field=models.IntegerField(
                editable=False, verbose_name="Количество заказов"
            ),
        ),
        migrations.AlterField(
            model_name="bouquet",
            name="amount_of_savings",
            field=models.IntegerField(
                editable=False, verbose_name="Количество добавлений в корзину"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="amount_of_orders",
            field=models.IntegerField(
                editable=False, verbose_name="Количество заказов"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="amount_of_savings",
            field=models.IntegerField(
                editable=False, verbose_name="Количество добавлений в корзину"
            ),
        ),
    ]
