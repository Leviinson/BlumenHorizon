# Generated by Django 5.1.3 on 2024-12-05 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "extended_contrib_models",
            "0018_extendedsite_city_ua_extendedsite_country_ua_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="extendedsite",
            old_name="city_ua",
            new_name="city_uk",
        ),
        migrations.RenameField(
            model_name="extendedsite",
            old_name="country_ua",
            new_name="country_uk",
        ),
        migrations.RenameField(
            model_name="extendedsite",
            old_name="header_alert_message_ua",
            new_name="header_alert_message_uk",
        ),
    ]
