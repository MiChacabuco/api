from pytz import timezone
from rest_framework import serializers
from rest_framework.fields import DateTimeField

from .models import PharmacyShift

utc_timezone = timezone("UTC")


class PharmacyShiftSerializer(serializers.ModelSerializer):
    start = DateTimeField(default_timezone=utc_timezone)
    end = DateTimeField(default_timezone=utc_timezone)

    class Meta:
        model = PharmacyShift
        fields = ("pharmacy", "start", "end")
