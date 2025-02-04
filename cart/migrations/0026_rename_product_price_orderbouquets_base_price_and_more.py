# Generated by Django 5.1.4 on 2025-02-02 17:19


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0025_alter_order_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderbouquets",
            old_name="product_price",
            new_name="base_price",
        ),
        migrations.RenameField(
            model_name="orderbouquets",
            old_name="product_discount",
            new_name="discount",
        ),
        migrations.RenameField(
            model_name="orderbouquets",
            old_name="product_discount_price",
            new_name="discount_price",
        ),
        migrations.RenameField(
            model_name="orderbouquets",
            old_name="product_tax_price",
            new_name="tax_price",
        ),
        migrations.RenameField(
            model_name="orderbouquets",
            old_name="product_tax_price_discounted",
            new_name="tax_price_discounted",
        ),
        migrations.RenameField(
            model_name="orderproducts",
            old_name="product_price",
            new_name="base_price",
        ),
        migrations.RenameField(
            model_name="orderproducts",
            old_name="product_discount",
            new_name="discount",
        ),
        migrations.RenameField(
            model_name="orderproducts",
            old_name="product_discount_price",
            new_name="discount_price",
        ),
        migrations.RenameField(
            model_name="orderproducts",
            old_name="product_tax_price",
            new_name="tax_price",
        ),
        migrations.RenameField(
            model_name="orderproducts",
            old_name="product_tax_price_discounted",
            new_name="tax_price_discounted",
        ),
        migrations.AddField(
            model_name="orderbouquets",
            name="taxes",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Всего заплаченных налогов",
            ),
            preserve_default=False,
        ),
    ]
