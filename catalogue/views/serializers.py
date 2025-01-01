from rest_framework import serializers

from core.services.utils import build_absolute_uri

from ..models import BouquetSize, BouquetSizeImage


class BouquetSizeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BouquetSizeImage
        fields = ("image",)

    def to_representation(self, instance):
        return build_absolute_uri(instance.image.url)


class BouquetSizeSerializer(serializers.ModelSerializer):
    images = BouquetSizeImageSerializer(many=True, read_only=True)

    class Meta:
        model = BouquetSize
        fields = (
            "id",
            "price",
            "discount_price",
            "discount",
            "diameter",
            "amount_of_flowers",
            "images",
        )
