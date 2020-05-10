from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet


class IsPharmacyFilter(SimpleListFilter):
    title = "farmacias"
    parameter_name = "pharmacy"

    def lookups(self, request, model_admin):
        return [
            (True, "Sólo farmacias"),
            (False, "Todo menos farmacias"),
        ]

    def queryset(self, request, queryset: QuerySet):
        value = self.value()
        if value is not None:
            filter = {"tags__value": "farmacias"}
            if value:
                return queryset.filter(**filter)
            else:
                return queryset.exclude(**filter)
