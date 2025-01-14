from typing import NamedTuple, NewType, TypedDict

RelativeUrl = NewType("RelativeUrl", str)
AbsoluteUrl = NewType("AbsoluteUrl", str)

# По какому полю сортировать queryset
OrderedModelField = NewType("OrderedModelField", str)

Limit = NewType("Limit", int)


class CanonicalLink(TypedDict):
    rel: str
    href: str


class AlternateLink(CanonicalLink):
    hreflang: str


class XDefaultLink(AlternateLink):
    pass


class AvailableLanguage(NamedTuple):
    lang_code: str
    lang_name: str
