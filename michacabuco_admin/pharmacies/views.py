from dynamic_rest.viewsets import WithDynamicViewSetMixin
from rest_framework import viewsets, mixins

from .models import PharmacyShift
from .serializers import PharmacyShiftSerializer


class PharmacyShiftViewSet(
    WithDynamicViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = PharmacyShiftSerializer

    def get_queryset(self, **kwargs):
        return PharmacyShift.objects.get_unfinished()
