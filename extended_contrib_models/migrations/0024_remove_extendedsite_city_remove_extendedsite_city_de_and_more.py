# Generated by Django 5.1.4 on 2025-01-19 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extended_contrib_models', '0023_alter_extendedsite_header_alert_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendedsite',
            name='city',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='city_de',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='city_en',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='city_ru',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='city_uk',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='country',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='country_de',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='country_en',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='country_ru',
        ),
        migrations.RemoveField(
            model_name='extendedsite',
            name='country_uk',
        ),
    ]
