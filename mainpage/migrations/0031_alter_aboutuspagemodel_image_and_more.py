# Generated by Django 5.1.3 on 2024-11-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0030_aboutuspagemodel_description_de_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutuspagemodel",
            name="image",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AlterField(
            model_name="contactspagemodel",
            name="image",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AlterField(
            model_name="deliverypagemodel",
            name="image",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AlterField(
            model_name="faqpagemodel",
            name="image",
            field=models.ImageField(
                default="defaults/no-image.webp",
                help_text="1000px/450px",
                upload_to="seoblock/",
                verbose_name="Картинка",
            ),
        ),
        migrations.AlterField(
            model_name="mainpageseoblock",
            name="image",
            field=models.ImageField(
                help_text="1000px/450px", upload_to="seoblock/", verbose_name="Картинка"
            ),
        ),
        migrations.AlterField(
            model_name="mainpagesliderimages",
            name="image",
            field=models.ImageField(
                help_text="1000px/450px",
                upload_to="mainpage-slider/",
                verbose_name="Фото на главном слайде",
            ),
        ),
    ]
