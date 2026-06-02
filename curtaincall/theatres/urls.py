from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Performance

@api_view(['POST'])
@permission_classes([AllowAny])
def temporary_create_play(request):
    try:
        # Вземаме данните от Next.js
        title = request.data.get('title', 'Неозаглавено представление')
        description = request.data.get('description', '')
        date_str = request.data.get('date')
        price = request.data.get('price', 0)
        tickets = request.data.get('available_tickets', 100)

        # Подсигуряваме числата, в случай че идват като празен стринг ""
        try: price = float(price)
        except: price = 0.0

        try: tickets = int(tickets)
        except: tickets = 100

        # ХАК: Създаваме обекта, като проверяваме как се казват полетата в модела ти.
        # Така няма значение дали е 'available_tickets' или само 'tickets', 'date' или 'start_time'
        p = Performance()
        
        # 1. Заглавие и Описание
        p.title = title
        if hasattr(p, 'description'): p.description = description

        # 2. Напасване на датата
        if hasattr(p, 'date'): p.date = date_str if date_str else datetime.datetime.now()
        elif hasattr(p, 'start_time'): p.start_time = date_str if date_str else datetime.datetime.now()

        # 3. Напасване на цената
        if hasattr(p, 'price'): p.price = price

        # 4. Напасване на билетите
        if hasattr(p, 'available_tickets'): p.available_tickets = tickets
        elif hasattr(p, 'tickets'): p.tickets = tickets
        elif hasattr(p, 'available_seats'): p.available_seats = tickets

        # Запазваме в базата
        p.save()

        return Response({
            "success": True,
            "message": "Представлението е създадено успешно!",
            "id": p.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("!!! КРИТИЧНА ГРЕШКА В ТЕРМИНАЛА !!!:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        title = request.data.get('title')
        description = request.data.get('description')
        date = request.data.get('date')
        price = request.data.get('price')
        available_tickets = request.data.get('available_tickets')

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

# Пътища
urlpatterns = [
    path('plays/', temporary_create_play, name='create_play'),
]