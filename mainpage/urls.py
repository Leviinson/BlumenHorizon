from django.urls import path

from .views import (  # AboutUsView,; DeliveryInstructionsView,; PaymentInstructionsView,; PublicAgreementView,; PrivacyAndPolicyView,
    MainPageView,
)

app_name = "mainpage"

urlpatterns = [
    path("", MainPageView.as_view(), name="offers"),
    # path("individual-order/", IndividualOrderView.as_view(), name="individual-order-negotiate"),
    # path("about/", AboutUsView.as_view(), name="about"),
    # path("delivery/", DeliveryInstructionsView.as_view(), name="delivery"),
    # path("payment/", PaymentInstructionsView.as_view(), name="payment"),
    # path("public-agreement/", PublicAgreementView.as_view(), name="public-agreement"),
    # path("privacy-and-policy/", PrivacyAndPolicyView.as_view(), name="privacy"),
]
