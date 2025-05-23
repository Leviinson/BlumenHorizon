# Generated by Django 5.1.2 on 2024-11-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="robotstxt",
            name="content",
            field=models.TextField(
                default="User-agent: *\nDisallow: /admin/\nDisallow: /cart/\nDisallow: /accounts/\nDisallow: /search/\nDisallow: /jsi18n/\nDisallow: /tinymce/\nDisallow: /tinymce-image-upload/\nDisallow: /logout/\nDisallow: /mainpage/individual-order/\nDisallow: /catalog/individual-question/\nDisallow: /catalog/*?min_price=\nDisallow: /catalog/*?max_price=\nDisallow: /catalog/*?min_diameter=\nDisallow: /catalog/*?max_diameter=\nDisallow: /catalog/*?min_amount_of_flowers=\nDisallow: /catalog/*?max_amount_of_flowers=\nDisallow: /catalog/*?colors=\nDisallow: /catalog/*?flowers=\nSitemap: `https://www`.blumenhorizon.com/sitemap.xml\n"
            ),
        ),
    ]
