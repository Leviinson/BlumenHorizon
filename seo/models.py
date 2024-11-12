# seo/models.py
from django.db import models


class RobotsTxt(models.Model):
    content = models.TextField(
        default="""User-agent: *
Disallow: /admin/
Disallow: /cart/
Disallow: /accounts/
Disallow: /search/
Disallow: /jsi18n/
Disallow: /tinymce/
Disallow: /tinymce-image-upload/
Disallow: /logout/
Disallow: /mainpage/individual-order/
Disallow: /catalog/individual-question/
Disallow: /catalog/*?min_price=
Disallow: /catalog/*?max_price=
Disallow: /catalog/*?min_diameter=
Disallow: /catalog/*?max_diameter=
Disallow: /catalog/*?min_amount_of_flowers=
Disallow: /catalog/*?max_amount_of_flowers=
Disallow: /catalog/*?colors=
Disallow: /catalog/*?flowers=
Sitemap: https://www.blumenhorizon.com/sitemap.xml
"""
    )

    def __str__(self):
        return "Robots.txt Content"


class SitemapPage(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    last_modified = models.DateTimeField(auto_now=True)
    changefreq = models.CharField(max_length=20, default="weekly")
    priority = models.FloatField(default=0.5)

    def __str__(self):
        return self.name
