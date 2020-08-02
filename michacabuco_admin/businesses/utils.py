import re
from os import environ

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def notify_business_modification(business: "Business", created: bool):
    verb = "creado" if created else "modificado"
    url = reverse("admin:businesses_business_change", args=[business.id])
    url = f"{environ['BASE_URL']}{url}"
    message = f'El negocio "{business.name}" fue {verb}.'
    html = (
        f'El negocio <a href="{url}" target="_blank">"{business.name}"</a> fue {verb}.'
    )
    send_mail(
        f"Negocio {verb}",
        message,
        None,
        [email for _, email in settings.ADMINS],
        html_message=html,
    )


def instagram_url_to_username(url: str):
    """Convert Instagram URL to username"""
    url_match = re.search("instagram.com/([^?/]+)", url)
    if url_match:
        try:
            instagram_username = url_match.group(1)
            return instagram_username
        except IndexError:
            pass
    return url
