import uuid

from django.contrib.gis.db import models
from model_utils.models import TimeStampedModel

from .tasks import set_business_point, set_business_facebook
from .utils import instagram_url_to_username
from .validators import validate_image_size
from michacabuco_admin.users.models import User


class Tag(models.Model):
    value = models.CharField("valor", max_length=255, unique=True)

    def __str__(self):
        return self.value

    class Meta:
        ordering = ["value"]


class Business(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("nombre", max_length=255, db_index=True)
    summary = models.TextField(
        "descripción", blank=True, help_text="Describa en pocas palabras su negocio."
    )
    avatar = models.ImageField(
        "avatar",
        upload_to="avatars",
        blank=True,
        null=True,
        help_text="Logo o imagen de su comercio/negocio. Tamaño máximo: 5MB.",
        validators=[validate_image_size],
    )
    address = models.CharField(
        "dirección",
        max_length=255,
        blank=True,
        help_text="Dirección física de su negocio (calle + número).",
    )
    point = models.PointField(
        "coordenadas", blank=True, null=True, help_text="longitud | latitud"
    )
    instagram = models.CharField("Instagram", max_length=255, blank=True)
    facebook = models.CharField("Facebook", max_length=255, blank=True)
    email = models.CharField("email", max_length=255, blank=True)
    website = models.CharField("página web", max_length=255, blank=True)
    has_delivery = models.BooleanField(
        "¿Realiza delivery?", default=False, help_text="Sólo aplica para comercios.",
    )
    tags = models.ManyToManyField(Tag, blank=True)
    is_useful = models.BooleanField("¿Es número útil?", default=False)
    is_visible = models.BooleanField("¿Es visible?", default=False)
    created_by = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="creado por",
        related_name="businesses",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "negocio"
        verbose_name_plural = "negocios"

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.instagram = instagram_url_to_username(self.instagram)

        if not self.address:
            # Clear point when the address is removed
            self.point = None
        else:
            # Async task to set point
            set_business_point.delay(self.id, self.address)

        # Async task to set Facebook
        set_business_facebook.delay(self.id, self.facebook)

        super().save(**kwargs)


class BusinessPhone(models.Model):
    business = models.ForeignKey(Business, models.CASCADE, related_name="phones")
    number = models.CharField(
        "número", max_length=17, help_text="Ejemplo: (02352) 15-123456"
    )
    is_whatsapp = models.BooleanField(
        "¿Es de WhatsApp?",
        default=False,
        help_text="Marcar si es un número de WhatsApp.",
    )

    class Meta:
        verbose_name = "número de teléfono"
        verbose_name_plural = "números de teléfono"

    def __str__(self):
        return str(self.number)
