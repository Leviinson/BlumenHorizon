# Generated by Django 5.1.3 on 2024-11-20 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0026_aboutuspagemodel_description_en_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deliverypagemodel",
            name="meta_tags_en",
        ),
        migrations.RemoveField(
            model_name="deliverypagemodel",
            name="meta_tags_ru",
        ),
    ]
