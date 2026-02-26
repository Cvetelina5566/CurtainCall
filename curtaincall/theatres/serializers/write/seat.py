from rest_framework import serializers
from ..models import Seat

class SeatSerializer(serializers.ModelSerializer):
    hall_id = serializers.IntegerField()

    class Meta:
        model = Seat
        fields = [
            "id",
            "row",
            "number",
            "hall_id",
        ]
