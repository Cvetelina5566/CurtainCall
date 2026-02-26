from rest_framework import serializers
from ..models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    performance_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "performance_id",
            "seat_id",
            "price",
            "is_sold",
        ]
