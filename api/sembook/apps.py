from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.sembook"

    def ready(self):
        import api.sembook.signals
