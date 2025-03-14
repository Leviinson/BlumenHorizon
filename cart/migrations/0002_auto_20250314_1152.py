import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="Order",
            name="delivery_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="С налогом",
                max_digits=10,
                null=True,
                verbose_name="Стоимость доставки",
            ),
        ),
        migrations.AddField(
            model_name="Order",
            name="delivery_vat_rate",
            field=models.IntegerField(
                blank=True,
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="Процент НДС на доставку",
            ),
        ),
    ]