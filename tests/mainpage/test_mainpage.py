from django.contrib.sites.models import Site
from django.template import Context
from django.test import Client

from ..types import UrlsDataclass


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
        )

    def _assert_mainpage_context(
        self,
        context: Context,
        site_domain: str,
        site_name: str,
    ) -> None:
        assert context["domain_name"] == site_domain
        assert context["site_name"] == site_name
        assert (
            context["json_ld_description"]
            == "Blumen Horizon интернет-магазин цветов и подарков в Берлине"
        )
