# Generated by Django 5.1.2 on 2024-11-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0018_alter_mainpagemetatags_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainpagemetatags",
            name="meta_tags",
            field=models.TextField(max_length=1000, verbose_name="Мета-теги"),
        ),
    ]
