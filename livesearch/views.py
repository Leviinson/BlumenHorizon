from django.http import HttpRequest, JsonResponse

from catalogue.models import Bouquet, Product

def live_search(request: HttpRequest) -> JsonResponse:
    data = {"results": {"products": [], "bouquets": []}}
    if query := request.GET.get("q", ""):
        product_results = Product.objects.select_related("subcategory__category").only("name", "subcategory__category__name").filter(name__icontains=query)[:10]
        data["results"]["products"] = [
            {"name": product.name, "url": product.get_detail_url()}
            for product in product_results
        ]

        bouquet_results = Bouquet.objects.only("name").filter(name__icontains=query)[:10]
        data["results"]["bouquets"] = [
            {"name": bouquet.name, "url": bouquet.get_detail_url()}
            for bouquet in bouquet_results
        ]
    return JsonResponse(data)
