# Generated by Django 5.1.4 on 2024-12-16 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0043_alter_mainpagemodel_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="aboutuspagemodel",
            options={
                "verbose_name": "Страница «О нас»",
                "verbose_name_plural": "Страница «О нас»",
            },
        ),
        migrations.AlterModelOptions(
            name="contactspagemodel",
            options={
                "verbose_name": "Страница «Контакты»",
                "verbose_name_plural": "Страница «Контакты»",
            },
        ),
        migrations.AlterModelOptions(
            name="deliverypagemodel",
            options={
                "verbose_name": "Страница «Доставка»",
                "verbose_name_plural": "Страница «Доставка»",
            },
        ),
        migrations.AlterModelOptions(
            name="faqpagemodel",
            options={
                "verbose_name": "Страница «Частозадаваемые вопросы»",
                "verbose_name_plural": "Страница «Частозадаваемые вопросы»",
            },
        ),
        migrations.AlterModelOptions(
            name="impressumpagemodel",
            options={
                "verbose_name": "Страница «Правовая информация»",
                "verbose_name_plural": "Страница «Правовая информация»",
            },
        ),
        migrations.AlterModelOptions(
            name="mainpagesliderimages",
            options={
                "verbose_name": "Фото слайдера вверху главной страницы",
                "verbose_name_plural": "Фотографии слайдера вверху главной страницы",
            },
        ),
    ]
