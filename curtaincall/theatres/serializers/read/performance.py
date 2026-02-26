from rest_framework import serializers
from ...models import Performance
from .play import PlayReadSerializer
from .hall import HallReadSerializer


class PerformanceReadSerializer(serializers.ModelSerializer):
    play = PlayReadSerializer(read_only=True)
    hall = HallReadSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = [
            "id",
            "date",
            "time",
            "play",
            "hall",
        ]
