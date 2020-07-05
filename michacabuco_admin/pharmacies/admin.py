from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .models import PharmacyShift, PharmacyShiftLegacy, Pharmacy


class AbstractPharmacyShiftAdmin(admin.ModelAdmin):
    list_display = ["pharmacy_name", "start", "end"]
    list_select_related = ["pharmacy"]
    list_filter = [("pharmacy", RelatedDropdownFilter)]
    exclude = ["end"]

    def pharmacy_name(self, shift) -> str:
        return shift.pharmacy.name

    pharmacy_name.short_description = "farmacia"


@admin.register(PharmacyShift)
class PharmacyShiftAdmin(AbstractPharmacyShiftAdmin):
    def get_queryset(self, request):
        return PharmacyShift.objects.get_unfinished()


# TODO: Legacy, delete after a while.
@admin.register(PharmacyShiftLegacy)
class PharmacyShiftLegacyAdmin(AbstractPharmacyShiftAdmin):
    def get_queryset(self, request):
        return PharmacyShiftLegacy.objects.get_unfinished()


# TODO: Legacy, delete after a while.
@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id")
