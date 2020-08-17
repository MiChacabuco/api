from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from pytz import timezone
from rest_framework import serializers
from rest_framework.fields import DateTimeField

from michacabuco_admin.businesses.serializers import BusinessSerializer
from .models import PharmacyShift

utc_timezone = timezone("UTC")


class PharmacyShiftSerializer(DynamicModelSerializer):
    pharmacy = DynamicRelationField(BusinessSerializer, embed=True)
    start = DateTimeField(default_timezone=utc_timezone)
    end = DateTimeField(default_timezone=utc_timezone)

    class Meta:
        model = PharmacyShift
        fields = ["pharmacy", "start", "end"]
