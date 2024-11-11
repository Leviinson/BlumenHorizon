# Generated by Django 5.1.2 on 2024-11-11 00:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0013_bouquetssizes_rename_size_bouquet_diameter_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bouquetssizes",
            name="discount",
            field=models.IntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="Скидка",
            ),
        ),
    ]
