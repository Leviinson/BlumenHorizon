# Generated by Django 5.1.2 on 2024-11-14 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0027_alter_bouquet_colors_alter_bouquet_flowers_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="color",
            options={
                "verbose_name": "Цвет букета",
                "verbose_name_plural": "Цветовые гаммы букетов",
            },
        ),
        migrations.AlterModelOptions(
            name="flower",
            options={"verbose_name": "Цветок", "verbose_name_plural": "Состав букетов"},
        ),
    ]
