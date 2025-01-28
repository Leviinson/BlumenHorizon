from ..caching import set_or_get_from_cache


class SiteRepository:
    @classmethod
    def get_domain(cls):
        return set_or_get_from_cache("site_domain", 60 * 15)

    @classmethod
    def get_name(cls):
        return set_or_get_from_cache("site_name", 60 * 15)

    @classmethod
    def get_email(cls):
        return set_or_get_from_cache("site_email", 60 * 15)

    @classmethod
    def get_currency_code(cls):
        return set_or_get_from_cache("currency_code", 60 * 15)

    @classmethod
    def get_currency_symbol(cls):
        return set_or_get_from_cache("currency_symbol", 60 * 15)

    @classmethod
    def get_tax_percent(cls):
        return set_or_get_from_cache(
            "tax_percent",
            60 * 15,
        )

    @classmethod
    def get_country(cls):
        return set_or_get_from_cache("country_name", 60 * 15)

    @classmethod
    def get_country_code(cls):
        return set_or_get_from_cache("country_code", 60 * 15)

    @classmethod
    def get_city(cls):
        return set_or_get_from_cache("city_name", 60 * 15)

    @classmethod
    def get_socials(cls):
        return set_or_get_from_cache("socials", 60 * 15)

    @classmethod
    def get_alert_message(cls):
        return set_or_get_from_cache("header_alert_message", 60 * 15)
