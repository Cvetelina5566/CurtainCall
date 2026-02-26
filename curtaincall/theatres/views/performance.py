from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..services.performance_service import get_all_performances, get_performance_by_id
from ..serializers.read.performance import PerformanceReadSerializer
from ..serializers.write.performance import PerformanceWriteSerializer
from ..models.performance import Performance
from ..models.play import Play
from ..models.hall import Hall


from rest_framework.permissions import AllowAny, IsAuthenticated

class PerformanceListAPIView(APIView):
    """
    GET: Public listing of all performances
    POST: Only PR users (theater_manager role) can create
    """

    # Default: require authentication for everything
    permission_classes = [AllowAny]
    authentication_classes = []  # <-- disable JWT auth completely

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_authenticators(self):
        """
        Disable authentication for GET requests (public endpoint)
        """
        if self.request.method == "GET":
            return []  # No authentication
        return super().get_authenticators()  # Use default JWT for POST

    def get(self, request):
        performances = get_all_performances()
        serializer = PerformanceReadSerializer(performances, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not hasattr(user, "role") or user.role != "theater_manager":
            return Response(
                {"detail": "Only PR users can create performances."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PerformanceWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Play.objects.get(id=serializer.validated_data["play_id"])
            Hall.objects.get(id=serializer.validated_data["hall_id"])
        except (Play.DoesNotExist, Hall.DoesNotExist):
            return Response(
                {"detail": "Play or Hall not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        performance = serializer.save()
        read_serializer = PerformanceReadSerializer(performance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)



from rest_framework.permissions import AllowAny

class PerformanceDetailAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # explicitly public

    def get(self, request, pk):
        try:
            performance = get_performance_by_id(pk)
        except Performance.DoesNotExist:
            return Response(
                {"detail": "Performance not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PerformanceReadSerializer(performance)
        return Response(serializer.data)
