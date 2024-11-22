# Generated by Django 5.1.3 on 2024-11-22 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("extended_contrib_models", "0012_alter_extendedsite_tax_percent"),
    ]

    operations = [
        migrations.AddField(
            model_name="extendedsite",
            name="account_name",
            field=models.CharField(
                default="Vitalii Melnykov", max_length=40, verbose_name="Название счёта"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="extendedsite",
            name="iban",
            field=models.CharField(
                default="DE3467192873123", max_length=50, verbose_name="IBAN для оплаты"
            ),
            preserve_default=False,
        ),
    ]
