from typing import Optional

from django.utils.translation import override

from core.services.types import AbsoluteUrl
from core.services.utils.urls import build_absolute_url

from ..abstract import CanonicalLinksAbstract
from ..types import AlternateLink, AvailableLanguage, CanonicalLink, XDefaultLink


class CanonicalLinksMixin(CanonicalLinksAbstract):

    def get_context_data(self, *args, **kwargs):
        if not self.relative_url:
            raise NotImplementedError("Attribute “relative_url” must be specified.")
        return super().get_context_data(*args, **kwargs)

    def get_canonical_link(self, current_lang_code: str) -> CanonicalLink:
        """
        Генерирует canonical ссылку для каталога.

        Этот метод:
        - Создаёт ссылку, указывающую на каноническую версию страницы каталога.
        - Учитывает текущий язык при генерации ссылки.

        Аргументы:
            current_lang_code (str): Код текущего языка, для которого генерируется каноническая ссылка.

        Возвращает:
            CanonicalLink: Объект канонической ссылки с атрибутами `rel="canonical"` и `href`.
        """
        return CanonicalLink(
            rel="canonical",
            href=self.get_absolute_url(current_lang_code),
        )

    def get_alternate_links(
        self,
        current_lang_code: str,
        available_languages: list[AvailableLanguage],
    ) -> list[AlternateLink]:
        """
        Генерирует список alternate ссылок для каталога.

        Этот метод:
        - Создаёт список ссылок, указывающих на переводы страницы каталога на другие языки.
        - Исключает текущий язык из списка.

        Аргументы:
            current_lang_code (str): Код текущего языка.
            available_languages (list[AvailableLanguage]): Список доступных языков в формате
            [(код языка, название языка)].

        Возвращает:
            list[AlternateLink]: Список объектов alternate ссылок с атрибутами `rel`,
            `hreflang` и `href`.
        """
        result = []
        for lang_code, lang_name in available_languages:
            if lang_code == current_lang_code:
                continue
            result.append(
                AlternateLink(
                    rel="alternate",
                    hreflang=lang_code,
                    href=self.get_absolute_url(lang_code=lang_code),
                )
            )
        return result

    def get_xdefault_link(
        self,
        default_lang_code: str,
    ) -> XDefaultLink:
        """
        Генерирует x-default ссылку для каталога.

        Этот метод:
        - Создаёт ссылку с атрибутом `x-default`, указывающую на версию страницы для
        языкового предпочтения по умолчанию.

        Аргументы:
            default_lang_code (str): Код языка по умолчанию.

        Возвращает:
            XDefaultLink: Объект ссылки с атрибутами `rel="x-default"`, `hreflang`, и `href`.
        """
        return XDefaultLink(
            rel="x-default",
            hreflang=default_lang_code,
            href=self.get_absolute_url(default_lang_code),
        )

    def get_absolute_url(self, lang_code: Optional[str] = None) -> AbsoluteUrl:
        """
        Генерирует абсолютный URL для каталога.

        Этот метод:
        - Создаёт абсолютный URL для страницы каталога.
        - Опционально переключает язык для ссылки, используя параметр `lang_code`.
        - Использует контекстный менеджер `override` для временного изменения языка,
        чтобы избежать глобального влияния на текущий запрос.

        Аргументы:
            lang_code (Optional[str]): Код языка, для которого требуется создать ссылку.
            Если не указан, используется текущий язык запроса.

        Возвращает:
            AbsoluteUrl: Абсолютный URL для страницы каталога.
        """
        if lang_code:
            with override(lang_code):
                return build_absolute_url(
                    self.relative_url,
                )
        return build_absolute_url(
            self.relative_url,
        )
