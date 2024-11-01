from django.db import models

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    stripe_code = models.TextChoices(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
