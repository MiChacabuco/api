from django.apps import AppConfig


class BusinessesConfig(AppConfig):
    name = "michacabuco_admin.businesses"
    verbose_name = "Negocios"

    def ready(self):
        try:
            from . import signals  # noqa F401
        except ImportError:
            pass
