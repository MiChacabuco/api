from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

from michacabuco_admin.users.serializers import UserSerializer
from .models import EventDate, Event


class EventSerializer(DynamicModelSerializer):
    created_by = DynamicRelationField(UserSerializer, deferred=True, embed=True)

    class Meta:
        model = Event
        fields = ["id", "title", "body", "image", "youtube", "created_by"]


class EventDateSerializer(DynamicModelSerializer):
    event = DynamicRelationField(EventSerializer)

    class Meta:
        model = EventDate
        fields = ["event", "start", "end"]
