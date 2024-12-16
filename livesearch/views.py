import hashlib
from collections import defaultdict

from django.core.cache import cache
from django.http import HttpRequest, JsonResponse

from catalogue.models import Bouquet, Product


def generate_cache_key(query: str) -> str:
    query_hash = hashlib.md5(query.encode("utf-8")).hexdigest()
    return f"search_results_{query_hash}"


def perform_search(query: str) -> dict:
    data = {"results": {"products": defaultdict(list), "bouquets": defaultdict(list)}}

    for model, key in [(Product, "products"), (Bouquet, "bouquets")]:
        results = (
            model.objects.select_related("subcategory__category", "subcategory")
            .only(
                "name",
                "subcategory__category__name",
                "subcategory__slug",
                "subcategory__category__slug",
                "slug",
            )
            .filter(name__icontains=query)[:10]
        )
        for item in results:
            category_name = item.subcategory.category.name
            data["results"][key][category_name].append(
                {"name": item.name, "url": item.get_relative_url()}
            )

    return data


def live_search(request: HttpRequest) -> JsonResponse:
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"results": {"products": {}, "bouquets": {}}})

    cache_key = generate_cache_key(query)
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data)

    data = perform_search(query)
    cache.set(cache_key, data, timeout=60 * 60)
    return JsonResponse(data)
