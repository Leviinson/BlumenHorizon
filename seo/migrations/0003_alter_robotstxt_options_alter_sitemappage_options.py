# Generated by Django 5.1.2 on 2024-11-14 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("seo", "0002_alter_robotstxt_content"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="robotstxt",
            options={"verbose_name": "robots.txt", "verbose_name_plural": "robots.txt"},
        ),
        migrations.AlterModelOptions(
            name="sitemappage",
            options={
                "verbose_name": "sitemap.xml",
                "verbose_name_plural": "sitemap.xml",
            },
        ),
    ]
