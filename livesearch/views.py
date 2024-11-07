from collections import defaultdict

from django.http import HttpRequest, JsonResponse

from catalogue.models import Bouquet, Product


def live_search(request: HttpRequest) -> JsonResponse:
    data = {"results": {"products": defaultdict(list), "bouquets": defaultdict(list)}}

    if query := request.GET.get("q", ""):
        # Получение результатов продуктов и группировка по категориям
        product_results = (
            Product.objects.select_related("subcategory__category")
            .only("name", "subcategory__category__name")
            .filter(name__icontains=query)[:10]
        )

        # Группируем продукты по категориям
        for product in product_results:
            category_name = product.subcategory.category.name  # Получаем имя категории
            data["results"]["products"][category_name].append(
                {"name": product.name, "url": product.get_detail_url()}
            )

        # Получение результатов букетов и группировка по категориям
        bouquet_results = (
            Bouquet.objects.select_related("subcategory__category")
            .only("name", "subcategory__category__name")
            .filter(name__icontains=query)[:10]
        )

        # Группируем букеты по категориям
        for bouquet in bouquet_results:
            category_name = bouquet.subcategory.category.name  # Получаем имя категории
            data["results"]["bouquets"][category_name].append(
                {"name": bouquet.name, "url": bouquet.get_detail_url()}
            )

    # Преобразуем defaultdict в обычный dict перед возвратом ответа
    data["results"]["products"] = dict(data["results"]["products"])
    data["results"]["bouquets"] = dict(data["results"]["bouquets"])

    return JsonResponse(data)
