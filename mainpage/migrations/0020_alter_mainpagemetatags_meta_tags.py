# Generated by Django 5.1.2 on 2024-11-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0019_alter_mainpagemetatags_meta_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainpagemetatags",
            name="meta_tags",
            field=models.TextField(
                default="<title>BlumenHorizon | </title>",
                max_length=1000,
                verbose_name="Мета-теги",
            ),
        ),
    ]
