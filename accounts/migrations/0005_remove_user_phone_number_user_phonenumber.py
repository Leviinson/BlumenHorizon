# Generated by Django 5.1.2 on 2024-10-19 09:50

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_user_first_name_alter_user_is_active_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="phone_number",
        ),
        migrations.AddField(
            model_name="user",
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
