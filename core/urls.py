"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path, re_path

service_urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("admin/", admin.site.urls),

    path("logout/", LogoutView.as_view(), name="logout"),
]

i18n_urlpatterns = i18n_patterns(
    path("accounts/", include("accounts.urls")),
    path("products/", include("catalogue.urls.products")),
    path("bouquets/", include("catalogue.urls.bouquets")),
    path("catalogue/", include("catalogue.urls.catalogue")),
    prefix_default_language=False
)

urlpatterns = service_urlpatterns + i18n_urlpatterns

if settings.DEBUG and not settings.TESTING:
    urlpatterns.extend(debug_toolbar_urls())

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

from django.conf.urls.static import static

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
