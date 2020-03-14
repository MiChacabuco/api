from rest_framework import viewsets

from .models import PharmacyShift
from .serializers import PharmacyShiftSerializer


class PharmacyShiftViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacyShiftSerializer

    def get_queryset(self):
        return PharmacyShift.objects.get_unfinished()
