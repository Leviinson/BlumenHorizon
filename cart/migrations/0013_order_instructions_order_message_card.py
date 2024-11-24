# Generated by Django 5.1.3 on 2024-11-24 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0012_alter_order_sub_total_alter_order_tax_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="instructions",
            field=models.TextField(
                max_length=800, null=True, verbose_name="Инструкции к доставке"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="message_card",
            field=models.TextField(
                max_length=10000, null=True, verbose_name="Записка к букету"
            ),
        ),
    ]
