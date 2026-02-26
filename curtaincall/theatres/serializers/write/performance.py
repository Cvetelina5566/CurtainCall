from rest_framework import serializers
from ...models import Performance

class PerformanceWriteSerializer(serializers.ModelSerializer):
    play_id = serializers.IntegerField()
    hall_id = serializers.IntegerField()

    class Meta:
        model = Performance
        fields = [
            "id",
            "play_id",
            "hall_id",
            "date",
            "time",
        ]

    def create(self, validated_data):
        return Performance.objects.create(**validated_data)
