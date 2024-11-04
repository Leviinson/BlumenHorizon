# Generated by Django 5.1.2 on 2024-11-03 17:38

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "extended_contrib_models",
            "0009_social_icon_hex_code_social_outline_hex_code_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="social",
            name="background_hex_code",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                help_text="Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат).",
                image_field=None,
                max_length=25,
                samples=None,
                verbose_name="HEX код цвета фона (#f4678a к примеру)",
            ),
        ),
        migrations.AlterField(
            model_name="social",
            name="icon_hex_code",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                help_text="Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат).",
                image_field=None,
                max_length=25,
                samples=None,
                verbose_name="HEX код цвета иконки (#f4678a к примеру)",
            ),
        ),
        migrations.AlterField(
            model_name="social",
            name="outline_hex_code",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                help_text="Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат).",
                image_field=None,
                max_length=25,
                samples=None,
                verbose_name="HEX код цвета обводки (#f4678a к примеру)",
            ),
        ),
    ]
