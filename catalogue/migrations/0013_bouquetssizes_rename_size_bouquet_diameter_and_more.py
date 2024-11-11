# Generated by Django 5.1.2 on 2024-11-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0012_alter_individualquestion_bouquet_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BouquetsSizes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount_of_flowers",
                    models.IntegerField(verbose_name="Количество цветов в букете"),
                ),
                ("diameter", models.IntegerField(verbose_name="Диаметр букета")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Цена размера до 10ти значений, два из которых плавающая запятая. Т.е. до 99999999.99",
                        max_digits=10,
                        verbose_name="Цена размера",
                    ),
                ),
            ],
            options={
                "verbose_name": "Размер букета",
                "verbose_name_plural": "Размеры букетов",
            },
        ),
        migrations.RenameField(
            model_name="bouquet",
            old_name="size",
            new_name="diameter",
        ),
        migrations.AlterField(
            model_name="bouquet",
            name="colors",
            field=models.ManyToManyField(
                help_text="Выберите какого цвета букет.",
                related_name="bouquet",
                to="catalogue.color",
                verbose_name="Цвета",
            ),
        ),
        migrations.AddField(
            model_name="bouquet",
            name="sizes",
            field=models.ManyToManyField(
                related_name="bouquet",
                to="catalogue.bouquetssizes",
                verbose_name="Размеры букета",
            ),
        ),
    ]
