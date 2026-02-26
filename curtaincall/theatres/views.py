from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Performance, Ticket

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_ticket(request):
    performance_id = request.data.get('performance_id')
    quantity = request.data.get('quantity', 1) 

    try:
        performance = Performance.objects.get(id=performance_id)
    except Performance.DoesNotExist:
        return Response({"error": "Представлението не е намерено."}, status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.create(
        user=request.user, 
        performance=performance,
        quantity=quantity
    )

    return Response({
        "message": "Успешно закупихте билет(и)!", 
        "ticket_id": ticket.id
    }, status=status.HTTP_201_CREATED)