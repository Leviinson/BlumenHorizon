# Generated by Django 5.1.3 on 2024-11-22 01:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0011_order_sub_total_order_tax_order_tax_percent_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="sub_total",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Без налога",
                max_digits=10,
                null=True,
                verbose_name="Чистая стоимость",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="tax",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Стоимость налога",
                max_digits=10,
                null=True,
                verbose_name="Налоговая стоимость",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="tax_percent",
            field=models.IntegerField(
                default=0,
                help_text="%",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="НДС",
            ),
        ),
    ]
