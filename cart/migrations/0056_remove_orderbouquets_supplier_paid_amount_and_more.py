# Generated by Django 5.1.4 on 2025-03-12 13:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0055_alter_order_user_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderbouquets",
            name="supplier_paid_amount",
        ),
        migrations.RemoveField(
            model_name="orderbouquets",
            name="supplier_paid_taxes",
        ),
        migrations.RemoveField(
            model_name="orderbouquets",
            name="supplier_vat_rate",
        ),
        migrations.RemoveField(
            model_name="orderproducts",
            name="supplier_paid_amount",
        ),
        migrations.RemoveField(
            model_name="orderproducts",
            name="supplier_paid_taxes",
        ),
        migrations.RemoveField(
            model_name="orderproducts",
            name="supplier_vat_rate",
        ),
        migrations.AddField(
            model_name="order",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="earned_orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Менеджер принёсший заказ",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
