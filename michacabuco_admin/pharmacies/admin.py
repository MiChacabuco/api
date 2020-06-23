from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .models import Pharmacy, PharmacyShift


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id"]


@admin.register(PharmacyShift)
class PharmacyShiftAdmin(admin.ModelAdmin):
    list_display = ["pharmacy_name", "start", "end"]
    list_select_related = ["pharmacy"]
    list_filter = [("pharmacy", RelatedDropdownFilter)]
    exclude = ["end"]

    def get_queryset(self, request):
        return PharmacyShift.objects.get_unfinished()

    def pharmacy_name(self, shift: PharmacyShift) -> str:
        return shift.pharmacy.name

    pharmacy_name.short_description = "farmacia"
