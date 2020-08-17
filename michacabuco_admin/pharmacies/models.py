from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from michacabuco_admin.businesses.models import Business


class PharmacyShiftManager(models.Manager):
    def get_unfinished(self):
        # Get shifts that didn't end yet
        return self.filter(end__gt=timezone.now())


def get_default_shift_start():
    now = timezone.localtime()
    # Shifts starts at 8:30 by default
    now = now.replace(hour=8, minute=30, second=0, microsecond=0)
    return now


class PharmacyShift(models.Model):
    pharmacy = models.ForeignKey(
        Business,
        models.CASCADE,
        limit_choices_to={"tags__value": "farmacias"},
        verbose_name="farmacia",
        related_name="+",
    )
    start = models.DateTimeField("inicio", default=get_default_shift_start)
    end = models.DateTimeField("fin")
    objects = PharmacyShiftManager()

    def clean(self):
        end = self.start + timedelta(days=1)
        if end <= timezone.now():
            raise ValidationError("La fecha debe ser en el futuro")
        self.end = end

    class Meta:
        ordering = ["start"]
        verbose_name = "turno de farmacia"
        verbose_name_plural = "turnos de farmacias"
