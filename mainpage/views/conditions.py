from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from core.services.mixins.views import CommonContextMixin

from ..models import (
    AGBPageModel,
    ImpressumPageModel,
    PrivacyAndPolicyPageModel,
    ReturnPolicyPageModel,
)


class ConditionsViewMixin(CommonContextMixin):
    """
    Реализация паттернов «Шаблонный метод и «Стратегия».

    Условиями называются страницы содержащие юридическую информация,
    в основном посвящённые информированию пользователя и процессе оформления
    заказа, условиях возврата, конфиденциальность и безопасность данных и т.д.
    """

    template_name = "mainpage/conditions.html"
    http_method_names = [
        "get",
    ]
    url = None
    page_model = None
    title: str | None = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        PageModel = self.page_model
        page = PageModel.objects.first()
        context["page"] = page
        context["meta_tags"] = page.meta_tags
        context["url"] = self.url
        context["title"] = self.title
        context["created_at"] = page.created_at
        context["updated_at"] = page.updated_at
        return context


class AGBView(ConditionsViewMixin, TemplateView):
    """
    Контроллер который показывает страницу «Условия и положения»
    """

    url = reverse_lazy("mainpage:agb")
    page_model = AGBPageModel
    title = _("Условия и положения")


class PrivacyAndPolicyView(ConditionsViewMixin, TemplateView):
    """
    Контроллер который показывает страницу «Политика конфиденциальности»
    """

    url = reverse_lazy("mainpage:privacy-and-policy")
    page_model = PrivacyAndPolicyPageModel
    title = _("Политика конфиденциальности")


class ImpressumView(ConditionsViewMixin, TemplateView):
    """
    Контроллер который показывает страницу «Условия и положения»
    """

    url = reverse_lazy("mainpage:impressum")
    page_model = ImpressumPageModel
    title = _("Контактная информация")


class ReturnPolicyView(ConditionsViewMixin, TemplateView):
    """
    Контроллер который показывает страницу «Условия возврата»
    """

    url = reverse_lazy("mainpage:return-policy")
    page_model = ReturnPolicyPageModel
    title = _("Условия возврата")
