from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from michacabuco_admin.events.views import EventDateViewSet, EventViewSet
from michacabuco_admin.pharmacies.views import PharmacyShiftViewSet
from michacabuco_admin.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("pharmacies/shifts", PharmacyShiftViewSet, basename="shifts")
router.register("events/dates", EventDateViewSet, basename="event-dates")
router.register("events", EventViewSet, basename="events")


app_name = "api"
urlpatterns = router.urls
