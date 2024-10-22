from django.apps import AppConfig


class ExtendedContribModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "extended_contrib_models"
    verbose_name = "Расширенные данные о встроенных нередактируемых моделях Django"
