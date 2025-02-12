# Generated by Django 5.1.4 on 2025-02-12 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0047_alter_refundreceipt_image_ordercreditadjustment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bankaccount",
            options={
                "verbose_name": "5. Банковский счёт",
                "verbose_name_plural": "5. Банковские счета",
            },
        ),
        migrations.AlterModelOptions(
            name="bill",
            options={"verbose_name": "2. Чек", "verbose_name_plural": "2. Чеки"},
        ),
        migrations.AlterModelOptions(
            name="florist",
            options={
                "verbose_name": "3. Флорист",
                "verbose_name_plural": "3. Флористы",
            },
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "1. Заказ", "verbose_name_plural": "1. Заказы"},
        ),
        migrations.AlterModelOptions(
            name="ordercreditadjustment",
            options={
                "verbose_name": "Корректировка (начисление)",
                "verbose_name_plural": "Корректировки (начисления)",
            },
        ),
        migrations.AlterModelOptions(
            name="orderdebitadjustment",
            options={
                "verbose_name": "Корректировка (возврат)",
                "verbose_name_plural": "Корректировки (возвраты)",
            },
        ),
        migrations.AlterModelOptions(
            name="refundreceipt",
            options={
                "verbose_name": "4. Чек возврата от флориста",
                "verbose_name_plural": "4. Чеки возвратов от флористов",
            },
        ),
        migrations.RemoveField(
            model_name="ordercreditadjustment",
            name="adjustment_type",
        ),
        migrations.RemoveField(
            model_name="orderdebitadjustment",
            name="adjustment_type",
        ),
    ]
