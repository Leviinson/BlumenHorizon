from django.db.models import OuterRef, Subquery


class ListViewMixin:
    allow_empty = True
    paginate_by = 8
    image_model = None
    image_model_related_name = None

    def get_queryset(self):
        qs = super().get_queryset()
        first_image_subquery = self.image_model.objects.filter(
            **{
                self.image_model_related_name: OuterRef("pk"),
            }
        ).order_by("id")[:1]

        return qs.filter(is_active=True, subcategory__is_active=True, subcategory__category__is_active=True).annotate(
            first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
        ).order_by("name")
