from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.encoding import filepath_to_uri
from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.fields import SerializerMethodField

from .models import Business, BusinessPhone


class PhonesSerializer(DynamicModelSerializer):
    class Meta:
        model = BusinessPhone
        fields = ["number", "is_whatsapp"]


class BusinessSerializer(DynamicModelSerializer):
    phones = DynamicRelationField(PhonesSerializer, many=True, embed=True)
    point = SerializerMethodField()
    avatar = SerializerMethodField()

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "summary",
            "avatar",
            "address",
            "point",
            "instagram",
            "facebook",
            "email",
            "website",
            "has_delivery",
            "phones",
            "is_useful",
        ]
        extra_kwargs = {
            # Necessary for filtering with Dynamic REST, hidden from output.
            "is_useful": {"write_only": True}
        }

    def get_point(self, business: Business):
        point: Point = business.point
        return [point.x, point.y] if point else None

    def get_avatar(self, business: Business):
        if not business.avatar:
            return None
        filepath = filepath_to_uri(business.avatar.name)
        return f"{settings.MEDIA_URL}{filepath}"

    def to_representation(self, instance):
        # Remove falsy values from the representation
        ret = super().to_representation(instance)
        # DynamicRest needs the same dict instance to be returned,
        # that's why we use del instead of dict comprehension.
        falsy_keys = [k for k, v in ret.items() if not v]
        for k in falsy_keys:
            del ret[k]

        # Add distance field
        try:
            ret["distance"] = round(instance.distance.m)
        except AttributeError:
            # No distance, don't do anything.
            pass

        return ret
