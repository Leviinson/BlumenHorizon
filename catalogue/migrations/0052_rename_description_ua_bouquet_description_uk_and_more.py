# Generated by Django 5.1.3 on 2024-12-05 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0051_bouquet_description_ua_bouquet_meta_tags_ua_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bouquet",
            old_name="description_ua",
            new_name="description_uk",
        ),
        migrations.RenameField(
            model_name="bouquet",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="bouquet",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="bouquet",
            old_name="slug_ua",
            new_name="slug_uk",
        ),
        migrations.RenameField(
            model_name="bouquet",
            old_name="specs_ua",
            new_name="specs_uk",
        ),
        migrations.RenameField(
            model_name="bouquetcategory",
            old_name="catalog_page_meta_tags_ua",
            new_name="catalog_page_meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="bouquetcategory",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="bouquetcategory",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="bouquetcategory",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="bouquetcategory",
            old_name="slug_ua",
            new_name="slug_uk",
        ),
        migrations.RenameField(
            model_name="bouquetimage",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="bouquetsizeimage",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="bouquetslistpagemodel",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="bouquetsubcategory",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="bouquetsubcategory",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="bouquetsubcategory",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="bouquetsubcategory",
            old_name="slug_ua",
            new_name="slug_uk",
        ),
        migrations.RenameField(
            model_name="catalogpagemodel",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="color",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="flower",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="description_ua",
            new_name="description_uk",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="slug_ua",
            new_name="slug_uk",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="specs_ua",
            new_name="specs_uk",
        ),
        migrations.RenameField(
            model_name="productcategory",
            old_name="catalog_page_meta_tags_ua",
            new_name="catalog_page_meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="productcategory",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="productcategory",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="productcategory",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="productcategory",
            old_name="slug_ua",
            new_name="slug_uk",
        ),
        migrations.RenameField(
            model_name="productimage",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="productslistpagemodel",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="productsubcategory",
            old_name="image_alt_ua",
            new_name="image_alt_uk",
        ),
        migrations.RenameField(
            model_name="productsubcategory",
            old_name="meta_tags_ua",
            new_name="meta_tags_uk",
        ),
        migrations.RenameField(
            model_name="productsubcategory",
            old_name="name_ua",
            new_name="name_uk",
        ),
        migrations.RenameField(
            model_name="productsubcategory",
            old_name="slug_ua",
            new_name="slug_uk",
        ),
    ]
