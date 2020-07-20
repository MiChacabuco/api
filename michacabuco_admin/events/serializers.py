from django.conf import settings
from django.utils.encoding import filepath_to_uri
from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.fields import SerializerMethodField

from michacabuco_admin.users.serializers import UserSerializer
from .models import EventDate, Event


class EventSerializer(DynamicModelSerializer):
    created_by = DynamicRelationField(UserSerializer, deferred=True, embed=True)
    image = SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "title", "body", "image", "youtube", "created_by"]

    def get_image(self, event: Event):
        if not event.image:
            return None
        filepath = filepath_to_uri(event.image.name)
        return f"{settings.MEDIA_URL}{filepath}"


class EventDateSerializer(DynamicModelSerializer):
    event = DynamicRelationField(EventSerializer)

    class Meta:
        model = EventDate
        fields = ["event", "start", "end"]
