from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny # <-- Добавихме AllowAny
from .models import Performance, Ticket

@api_view(['POST'])
@permission_classes([AllowAny]) # <-- ОТКЛЮЧЕНО! Всеки може да създава пиеса без токен
def create_play(request):
    try:
        title = request.data.get('title')
        description = request.data.get('description')
        date = request.data.get('date')
        price = request.data.get('price')
        available_tickets = request.data.get('available_tickets')

        # Създаваме записа в базата данни
        performance = Performance.objects.create(
            title=title,
            description=description,
            date=date,
            price=price,
            available_tickets=available_tickets
        )

        return Response({
            "success": True,
            "message": "Представлението е създадено успешно!",
            "id": performance.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Грешка при запис: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


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