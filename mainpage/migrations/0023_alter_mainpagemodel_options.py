# Generated by Django 5.1.2 on 2024-11-18 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0022_mainpagemodel_delete_mainpagemetatags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mainpagemodel",
            options={
                "verbose_name": "Мета-тег и разметка главной страницы",
                "verbose_name_plural": "Мета-теги и разметка главной страницы",
            },
        ),
    ]
