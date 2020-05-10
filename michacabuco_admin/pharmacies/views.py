from dynamic_rest.viewsets import WithDynamicViewSetMixin
from rest_framework import viewsets, mixins

from .models import PharmacyShift, PharmacyShiftLegacy
from .serializers import PharmacyShiftSerializer, PharmacyShiftLegacySerializer


class PharmacyShiftViewSet(
    WithDynamicViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = PharmacyShiftSerializer

    def get_queryset(self, **kwargs):
        return PharmacyShift.objects.get_unfinished()


# TODO: Legacy, delete after a while.
class PharmacyShiftLegacyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PharmacyShiftLegacySerializer

    def get_queryset(self):
        return PharmacyShiftLegacy.objects.get_unfinished()
