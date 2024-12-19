from django.urls import path

from .views import (
    AboutDeliveryView,
    AboutUsView,
    AGBView,
    ContactUsView,
    FAQView,
    ImpressumView,
    IndividualOrderView,
    MainPageView,
    PrivacyAndPolicyView,
    ReturnPolicyView,
)

app_name = "mainpage"

urlpatterns = [
    path("", MainPageView.as_view(), name="offers"),
    path(
        "individual-order/",
        IndividualOrderView.as_view(),
        name="individual-order-negotiate",
    ),
    path("about/", AboutUsView.as_view(), name="about"),
    path("delivery/", AboutDeliveryView.as_view(), name="delivery"),
    path("contact/", ContactUsView.as_view(), name="contact"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("agb/", AGBView.as_view(), name="agb"),
    path("datenschutz/", PrivacyAndPolicyView.as_view(), name="privacy-and-policy"),
    path("impressum/", ImpressumView.as_view(), name="impressum"),
    path("widerrufsbelehrung/", ReturnPolicyView.as_view(), name="return-policy"),
]
