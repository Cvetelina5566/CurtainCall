from rest_framework import serializers
from ..models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    ticket_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order_id",
            "ticket_id",
        ]
