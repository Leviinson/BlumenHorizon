from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from core.services.mixins.views import CommonContextMixin

from ..models import (
    AboutUsPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
)


class FillerViewMixin:
    """
    Реализация паттернов «Шаблонный метод и «Стратегия».

    Филлерами называются дополнительные страницы, в основном посвящённые
    информированию пользователя. К примеру как с нами связаться, как работает
    доставка и т.д.
    """

    template_name = "mainpage/filler.html"
    http_method_names = ["get"]
    page_model = None
    url = None

    def get_context_data(self, *args, **kwargs):
        if not any((self.page_model, self.url)):
            raise AttributeError(
                "Attributes “page_model” or “template_name” are not specified."
            )

        context = super().get_context_data(*args, **kwargs)
        page = self.page_model.objects.first()
        context["page"] = page
        context["meta_tags"] = page.meta_tags
        context["url"] = self.url
        return context


class AboutUsView(FillerViewMixin, CommonContextMixin, TemplateView):
    """
    Контроллер который показывает страницу «О нас»
    """

    page_model = AboutUsPageModel
    url = reverse_lazy("mainpage:about")


class AboutDeliveryView(FillerViewMixin, CommonContextMixin, TemplateView):
    """
    Контроллер который показывает страницу «Доставка»
    """

    page_model = DeliveryPageModel
    url = reverse_lazy("mainpage:delivery")


class ContactUsView(FillerViewMixin, CommonContextMixin, TemplateView):
    """
    Контроллер который показывает страницу «Контакты»
    """

    page_model = ContactsPageModel
    url = reverse_lazy("mainpage:contact")


class FAQView(FillerViewMixin, CommonContextMixin, TemplateView):
    """
    Контроллер который показывает страницу «Часто задаваемые вопросы».

    На данный момент этот контроллер не подключён к роутеру, так как
    контент для неё ещё не составлен.
    """

    page_model = FAQPageModel
    url = reverse_lazy("mainpage:faq")
