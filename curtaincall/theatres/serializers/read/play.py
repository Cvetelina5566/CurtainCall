from rest_framework import serializers
from ...models import Play
from .theatre import TheatreReadSerializer


class PlayReadSerializer(serializers.ModelSerializer):
    theatre = TheatreReadSerializer(read_only=True)

    class Meta:
        model = Play
        fields = [
            "id",
            "title",
            "description",
            "duration_minutes",
            "theatre",
        ]
