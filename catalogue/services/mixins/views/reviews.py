from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from catalogue.forms import BouquetReviewForm, ProductReviewForm
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.utils.first_image_attaching import annotate_first_image_and_alt


class CreateItemReviewViewMixin:
    form_class: BouquetReviewForm | ProductReviewForm
    template_name = "catalog/review.html"
    http_method_names = [
        "get",
        "post",
    ]
    queryset: QuerySet[Bouquet | Product] = None
    context_object_name = "item"
    slug_url_kwarg: str = None
    item_details_viewname: str = None
    image_model: BouquetImage | ProductImage

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["item_uri"] = reverse_lazy(
            self.item_details_viewname, kwargs=self.kwargs
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            review.item = self.object
            review.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(
            self.request,
            _(
                "Отзыв успешно отправлен на модерацию, благодарим за обратную связь ☺️",
            ),
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            self.item_details_viewname, args=self.args, kwargs=self.kwargs
        )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            queryset = annotate_first_image_and_alt(
                queryset, self.image_model, get_language()
            )
        try:
            obj = queryset.get(
                subcategory__category__slug=self.kwargs["category_slug"],
                subcategory__slug=self.kwargs["subcategory_slug"],
                slug=self.kwargs[self.slug_url_kwarg],
            )
        except queryset.model.DoesNotExist:
            raise Http404(
                _("Не найдено ни одного %(verbose_name)s совпадающего по запросу")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
