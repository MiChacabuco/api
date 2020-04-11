from rest_framework import viewsets, mixins

from .models import PharmacyShift
from .serializers import PharmacyShiftSerializer


class PharmacyShiftViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PharmacyShiftSerializer

    def get_queryset(self):
        return PharmacyShift.objects.get_unfinished()
