from django.urls import include, path
from rest_framework.routers import DefaultRouter
from views import stripe_webhook

router = DefaultRouter
router.register(r"webhook/", stripe_webhook)

urlpatterns = [
    path("", include(router.urls)),
]
