from rest_framework import serializers
from ...models import Hall
from .theatre import TheatreReadSerializer


class HallReadSerializer(serializers.ModelSerializer):
    theatre = TheatreReadSerializer(read_only=True)

    class Meta:
        model = Hall
        fields = [
            "id",
            "name",
            "capacity",
            "theatre",
        ]
