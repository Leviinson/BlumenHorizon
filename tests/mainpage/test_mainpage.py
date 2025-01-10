from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from django.template import Context
from django.test import Client

from extended_contrib_models.models import ExtendedSite, Social

from ..types import UrlsDataclass
from .conftest import EXPECTED_SOCIALS


class TestMainPage:
    def test_mainpage_context(
        self, client: Client, urls: UrlsDataclass, site: Site, mainpage
    ) -> None:
        response = client.get(urls.mainpage)
        assert response.status_code == 200

        self._assert_mainpage_context(
            context=response.context,
            site_domain=site.domain,
            site_name=site.name,
            site_extended=site.extended,
        )

    def _assert_mainpage_context(
        self,
        context: Context,
        site_domain: str,
        site_name: str,
        site_extended: ExtendedSite,
    ) -> None:
        assert context["domain_name"] == site_domain
        assert context["site_name"] == site_name
        assert (
            context["json_ld_description"]
            == "Blumen Horizon интернет-магазин цветов и подарков в Берлине"
        )
        assert context["company_email"] == settings.EMAIL_HOST_USER

        assert len(context["socials_right_bottom"]) == 3
        socials: QuerySet[Social] = context["socials_right_bottom"]
        for social, expected_social in zip(socials, EXPECTED_SOCIALS):
            assert social.absolute_url == expected_social["absolute_url"]
            assert social.background_hex_code == expected_social["background_hex_code"]
            assert social.bootstrap_icon == expected_social["bootstrap_icon"]
            assert social.extended_site == site_extended
            assert social.icon_hex_code == expected_social["icon_hex_code"]
            assert social.outline_hex_code == expected_social["outline_hex_code"]
