# Generated by Django 5.1.2 on 2024-11-14 00:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0015_alter_individualorder_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="individualorder",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="individual_orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Связанный аккаунт",
            ),
        ),
    ]
