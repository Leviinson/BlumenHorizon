# Generated by Django 5.1.4 on 2025-04-01 11:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_ordercreditadjustment_payment_system_fee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderbouquets",
            name="supplier_vat_rate",
            field=models.IntegerField(
                blank=True,
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="Ставка НДС от поставщика",
            ),
        ),
        migrations.AlterField(
            model_name="orderproducts",
            name="supplier_vat_rate",
            field=models.IntegerField(
                blank=True,
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="Ставка НДС от поставщика",
            ),
        ),
    ]
