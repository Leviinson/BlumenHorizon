# Generated by Django 5.1.3 on 2024-11-29 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "extended_contrib_models",
            "0016_extendedsite_country_iso_3166_1_alpha_2_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="extendedsite",
            name="country_iso_3166_1_alpha_2_de",
        ),
        migrations.RemoveField(
            model_name="extendedsite",
            name="country_iso_3166_1_alpha_2_en",
        ),
        migrations.RemoveField(
            model_name="extendedsite",
            name="country_iso_3166_1_alpha_2_ru",
        ),
    ]
