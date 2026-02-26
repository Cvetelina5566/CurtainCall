from rest_framework import serializers
from ...models import Play

class PlaySerializer(serializers.ModelSerializer):
    theatre_id = serializers.IntegerField()

    class Meta:
        model = Play
        fields = [
            "id",
            "title",
            "description",
            "duration_minutes",
            "theatre_id",
        ]

    def create(self, validated_data):
        return Play.objects.create(**validated_data)
