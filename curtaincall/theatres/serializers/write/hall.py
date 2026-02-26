from rest_framework import serializers
from models import Hall

class HallSerializer(serializers.ModelSerializer):
    theatre_id = serializers.IntegerField()

    class Meta:
        model = Hall
        fields = [
            "id",
            "name",
            "capacity",
            "theatre_id",
        ]
