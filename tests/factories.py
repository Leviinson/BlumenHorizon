import factory
import faker
from django.utils.text import slugify

from catalogue.models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    BouquetSubcategory,
    Color,
    Flower,
    Product,
    ProductCategory,
    ProductImage,
    ProductSubcategory,
)
from catalogue.models.services.abstract_models import MetaDataAbstractModel


class MetaDataAbstractModelFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=3)
    is_active = factory.Faker("boolean")
    amount_of_orders = factory.Faker("random_int", min=0, max=50)
    amount_of_savings = factory.Faker("random_int", min=0, max=50)
    meta_tags = factory.Faker("paragraph", nb_sentences=10)

    class Meta:
        model = MetaDataAbstractModel
        abstract = True

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class BouquetCategoryFactory(
    MetaDataAbstractModelFactory,
):
    class Meta:
        model = BouquetCategory


class BouquetSubcategoryFactory(
    MetaDataAbstractModelFactory,
):
    class Meta:
        model = BouquetSubcategory

    category = factory.SubFactory(BouquetCategoryFactory)


class ProductCategoryFactory(
    MetaDataAbstractModelFactory,
):
    class Meta:
        model = ProductCategory


class ProductSubcategoryFactory(
    MetaDataAbstractModelFactory,
):
    class Meta:
        model = ProductSubcategory

    category = factory.SubFactory(ProductCategoryFactory)


class ColorFactory(
    MetaDataAbstractModelFactory,
):
    class Meta:
        model = Color


class FlowerFactory(MetaDataAbstractModelFactory):
    class Meta:
        model = Flower


class BouquetFactory(
    MetaDataAbstractModelFactory,
):
    class Meta:
        model = Bouquet

    subcategory = factory.SubFactory(BouquetSubcategoryFactory)

    @factory.post_generation
    def colors(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for color in extracted:
                self.colors.add(color)
        else:
            self.colors.add(color)

    @factory.post_generation
    def flowers(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for flower in extracted:
                self.flowers.add(flower)
        else:
            self.flowers.add(FlowerFactory())


class BouquetImage(MetaDataAbstractModelFactory):
    class Meta:
        model = BouquetImage

    item = factory.SubFactory(BouquetFactory)


class ProductFactory(MetaDataAbstractModelFactory):
    class Meta:
        model = Product

    subcategory = factory.SubFactory(ProductSubcategoryFactory)


class ProductImage(MetaDataAbstractModelFactory):
    class Meta:
        model = ProductImage

    item = factory.SubFactory(ProductFactory)
