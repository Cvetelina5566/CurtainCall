from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from ..models import Theatre, Play, Hall
from ..serializers.read.theatre import TheatreReadSerializer
from ..serializers.read.play import PlayReadSerializer
from ..serializers.read.hall import HallReadSerializer
from ..serializers.write.play import PlaySerializer as PlayWriteSerializer


class TheatreListAPIView(APIView):
    """
    GET: Public list of theatres
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # disable JWT auth for GET

    def get(self, request):
        theatres = Theatre.objects.all().order_by("name")
        serializer = TheatreReadSerializer(theatres, many=True)
        return Response(serializer.data)


class PlayListAPIView(APIView):
    """
    GET: Public list of plays, filter by theatre_id
    POST: Only PR users (theater_manager) can create
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_authenticators(self):
        if self.request.method == "GET":
            return []  # disable authentication for GET
        return super().get_authenticators()

    def get(self, request):
        theatre_id = request.query_params.get("theatre_id")
        plays = Play.objects.all()
        if theatre_id:
            plays = plays.filter(theatre_id=theatre_id)
        plays = plays.order_by("title")
        serializer = PlayReadSerializer(plays, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "theater_manager":
            return Response(
                {"detail": "Only PR users can create plays."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PlayWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        play = serializer.save()
        read_serializer = PlayReadSerializer(play)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class HallListAPIView(APIView):
    """
    GET: Public list of halls, filter by theatre_id
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # disable JWT auth for GET

    def get(self, request):
        theatre_id = request.query_params.get("theatre_id")
        halls = Hall.objects.all()
        if theatre_id:
            halls = halls.filter(theatre_id=theatre_id)
        halls = halls.order_by("name")
        serializer = HallReadSerializer(halls, many=True)
        return Response(serializer.data)
