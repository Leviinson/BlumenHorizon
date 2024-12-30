from ..caching import set_or_get_from_cache


class SiteRepository:
    @classmethod
    def get_domain(cls):
        return set_or_get_from_cache("site_domain", 60 * 15)

    @classmethod
    def get_name(cls):
        return set_or_get_from_cache("site_name", 60 * 15)

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
        pass

    @classmethod
    def get_country_code(cls):
        pass

    @classmethod
    def get_city(cls):
        pass

    @classmethod
    def get_socials(cls):
        pass

    @classmethod
    def get_alert_message(cls):
        pass
