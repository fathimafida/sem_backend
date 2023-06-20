from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.authentication"

    def ready(self):
        import api.authentication.signals
