from dynamic_rest.viewsets import WithDynamicViewSetMixin
from rest_framework import mixins, viewsets

from .models import EventDate, Event
from .serializers import EventDateSerializer, EventSerializer


class EventViewSet(
    WithDynamicViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDateViewSet(
    WithDynamicViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    queryset = EventDate.objects.all()
    serializer_class = EventDateSerializer
