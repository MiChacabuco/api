from os import environ

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest
from django.urls import reverse

from config.middlewares import RequestMiddleware
from .models import Business


@receiver(post_save, sender=Business)
def notify_business_modification(sender, instance: Business, created: bool, **kwargs):
    request_middleware = RequestMiddleware()
    request: HttpRequest = request_middleware.thread_local.current_request
    if request.user.is_superuser:
        # The modification was done by an admin, don't send any email.
        return
    verb = "creado" if created else "modificado"
    url = reverse("admin:businesses_business_change", args=[instance.id])
    url = f"{environ['BASE_URL']}{url}"
    message = f'El negocio "{instance.name}" fue {verb}.'
    html = (
        f'El negocio <a href="{url}" target="_blank">"{instance.name}"</a> fue {verb}.'
    )
    send_mail(
        f"Negocio {verb}",
        message,
        None,
        [email for _, email in settings.ADMINS],
        html_message=html,
    )
