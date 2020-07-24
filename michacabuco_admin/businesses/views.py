import json

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Q
from dynamic_rest.viewsets import WithDynamicViewSetMixin
from rest_framework import viewsets, mixins

from .models import Business
from .serializers import BusinessSerializer


class BusinessViewSet(
    WithDynamicViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BusinessSerializer

    def get_queryset(self, queryset=None):
        # Get visible businesses
        qs = Business.objects.filter(is_visible=True)

        # Filter by name and tags
        query_params = self.request.query_params
        search = query_params.get("search")
        if search:
            words = search.split(" ")
            filters = Q(name__unaccent__icontains=search)
            for word in words:
                filters = filters | Q(tags__value__unaccent__startswith=word)
            qs = qs.filter(filters)

        # Order by distance
        point_from = query_params.get("point")
        if point_from:
            point_from = json.loads(point_from)
            point_from = Point(*point_from, srid=4326)
            qs = qs.annotate(distance=Distance("point", point_from)).order_by(
                "distance"
            )

        return qs
