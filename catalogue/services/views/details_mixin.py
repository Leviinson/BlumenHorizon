from typing import Any


class DetailViewMixin:
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        kwargs["title"] = self.object.name
        kwargs["images_url"] = (image.image.url for image in self.object.images.all())
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(subcategory__slug=self.kwargs["subcategory_slug"])