# Generated by Django 5.1.2 on 2024-11-12 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RobotsTxt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        default="User-agent: *\nDisallow: /admin/\nDisallow: /private/\nSitemap: https://www.blumenhorizon.com/sitemap.xml\n"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SitemapPage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("url", models.URLField()),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("changefreq", models.CharField(default="weekly", max_length=20)),
                ("priority", models.FloatField(default=0.5)),
            ],
        ),
    ]
