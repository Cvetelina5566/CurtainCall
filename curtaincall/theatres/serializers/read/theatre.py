from rest_framework import serializers
from ...models import Theatre


class TheatreReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = [
            "id",
            "name",
            "city",
            "address",
        ]
