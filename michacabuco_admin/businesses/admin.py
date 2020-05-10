from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.db.models import PointField
from django.db.models import TextField
from django.forms import Textarea
from django.http import HttpRequest

from .filters import IsPharmacyFilter
from .models import Business, BusinessPhone, Tag
from ..widgets import LatLongWidget


class BusinessPhoneInlineAdmin(admin.StackedInline):
    model = BusinessPhone
    extra = 1


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    search_fields = ["value"]


@admin.register(Business)
class BusinessAdmin(ModelAdmin):
    inlines = [BusinessPhoneInlineAdmin]
    list_filter = [IsPharmacyFilter]
    formfield_overrides = {
        PointField: {"widget": LatLongWidget},
        TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 60})},
    }
    autocomplete_fields = ["tags", "created_by"]
    search_fields = ["name"]

    def get_list_display(self, request: HttpRequest):
        fields = ["name"]
        if request.user.is_superuser:
            fields.append("is_visible")
        return fields

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        user = request.user
        if not user.is_superuser:
            # If not an admin, show only businesses the user owns.
            qs = qs.filter(created_by=user)
        return qs

    def get_fieldsets(self, request: HttpRequest, obj=None):
        required_fields = ["name"]
        optional_fields = [
            "summary",
            "avatar",
            "address",
            "has_delivery",
            "instagram",
            "facebook",
            "email",
            "website",
        ]
        fieldsets = [
            (None, {"fields": required_fields}),
            ("CAMPOS OPCIONALES", {"fields": optional_fields}),
        ]
        if request.user.is_superuser:
            # Show admin fields
            admin_fields = [
                "point",
                "tags",
                "is_useful",
                "is_visible",
                "created_by",
            ]
            admin_fieldset = ["VISIBLES POR ADMINS", {"fields": admin_fields}]
            fieldsets.append(admin_fieldset)
        return fieldsets

    def save_model(self, request: HttpRequest, business: Business, form, change: bool):
        if not change:
            # Link with the user that created the business
            business.created_by = request.user
        business.save()

    def has_delete_permission(self, request: HttpRequest, obj=None):
        return request.user.is_superuser

    class Media:
        # This is just to avoid a bug in django-admin-autocomplete
        pass
