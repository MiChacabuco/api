from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from michacabuco_admin.pharmacies.views import PharmacyShiftViewSet
from michacabuco_admin.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("pharmacies/shifts", PharmacyShiftViewSet, basename="shifts")


app_name = "api"
urlpatterns = router.urls
