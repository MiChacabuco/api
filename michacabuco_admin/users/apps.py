from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "michacabuco_admin.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import michacabuco_admin.users.signals  # noqa F401
        except ImportError:
            pass
