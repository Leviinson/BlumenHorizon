from typing import Any


class DetailViewMixin:
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["category_slug_breadcrumbs"] = self.object.subcategory.category.slug
        context["subcategory_slug_breadcrumbs"] = self.object.subcategory.slug
        return context