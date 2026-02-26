from rest_framework import serializers
from ..models import Order, OrderItem

class OrderItemInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "ticket_id"]

class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    items = OrderItemInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user_id",
            "created_at",
            "is_paid",
            "items",
        ]
