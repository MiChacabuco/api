from dynamic_rest.serializers import DynamicModelSerializer

from .models import User


class UserSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "name")
