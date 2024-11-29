# Generated by Django 5.1.3 on 2024-11-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0047_alter_bouquetslistpagemodel_json_ld_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bouquet",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquet",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquet",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquet",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetcategory",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetcategory",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetcategory",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetslistpagemodel",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetslistpagemodel",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetslistpagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetslistpagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetsubcategory",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetsubcategory",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetsubcategory",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="bouquetsubcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="catalogpagemodel",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="catalogpagemodel",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="catalogpagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="catalogpagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productslistpagemodel",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productslistpagemodel",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productslistpagemodel",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productslistpagemodel",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=1000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productsubcategory",
            name="meta_tags",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productsubcategory",
            name="meta_tags_de",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productsubcategory",
            name="meta_tags_en",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
        migrations.AlterField(
            model_name="productsubcategory",
            name="meta_tags_ru",
            field=models.TextField(
                default='<title>Blumen Horizon | </title>\n<meta name="description" content="Описание">',
                max_length=4000,
                null=True,
                verbose_name="Мета-теги",
            ),
        ),
    ]
