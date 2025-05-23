# Generated by Django 5.1.2 on 2024-11-07 22:42

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0007_alter_seoblock_options_individualorder_recall_me"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="individualorder",
            options={
                "verbose_name": "Индивидуальный заказ",
                "verbose_name_plural": "Индивидуальные заказы",
            },
        ),
        migrations.AlterField(
            model_name="individualorder",
            name="phonenumber",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=15,
                null=True,
                region=None,
                verbose_name="Номер телефона",
            ),
        ),
    ]
