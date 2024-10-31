from django.db.models import OuterRef, Subquery
from django.utils.translation import gettext_lazy as _


class ListViewMixin:
    allow_empty = True
    paginate_by = 8
    image_model = None
    image_model_related_name = None

    SORT_OPTIONS = [
        {"name": _("Цена по убыванию"), "value": "pd"},
        {"name": _("Цена по возрастанию"), "value": "pi"},
        {"name": _("По алфавиту"), "value": "alph"},
        {"name": _("Со скидкой"), "value": "disc"},
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        first_image_subquery = self.image_model.objects.filter(
            **{
                self.image_model_related_name: OuterRef("pk"),
            }
        ).order_by("id")[:1]

        sort_option = self.request.GET.get('sort', 'pd')
        
        match sort_option:
            case 'pd':
                qs = qs.order_by('-price')
            case 'pi':
                qs = qs.order_by('price')
            case 'alph':
                qs = qs.order_by('name')
            case 'disc':
                qs = qs.order_by('-discount')

        return (
            qs.filter(
                is_active=True,
                subcategory__is_active=True,
                subcategory__category__is_active=True,
            )
            .annotate(
                first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
            )
        )
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sort_options'] = self.SORT_OPTIONS
        return context
