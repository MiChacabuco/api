from django.db import models
from ckeditor.fields import RichTextField

from michacabuco_admin.users.models import User


def event_image_path(event: "Event", filename):
    return f"events/event_{event.id}/{filename}"


class Event(models.Model):
    title = models.CharField("título", max_length=255)
    body = RichTextField("cuerpo")
    image = models.ImageField(
        "imagen promocional", upload_to=event_image_path, blank=True, null=True
    )
    youtube = models.URLField(
        "video promocional (YouTube)", blank=True, help_text="Link a video de YouTube"
    )
    created_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventos"


class EventDate(models.Model):
    event = models.ForeignKey(
        Event, models.CASCADE, related_name="dates", verbose_name="evento"
    )
    start = models.DateTimeField("inicio")
    end = models.DateTimeField("fin")

    def __str__(self):
        date = self.start.astimezone()
        return date.strftime("%d/%m/%Y %H:%M")

    class Meta:
        ordering = ("start",)
        verbose_name = "fecha de evento"
        verbose_name_plural = "fechas de evento"
