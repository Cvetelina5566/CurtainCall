import datetime
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Performance, Hall, Theatre, Play 

@api_view(['POST'])
@permission_classes([AllowAny])
def temporary_create_play(request):
    try:
        title = request.data.get('title', 'Неозаглавено представление')
        description = request.data.get('description', '')
        date_str = request.data.get('date')
        price = request.data.get('price', 0)

        try: price = float(price)
        except: price = 0.0

        # Разделяме датата и часа
        date_val = datetime.date.today().strftime('%Y-%m-%d')
        time_val = "19:00:00"

        if date_str and "T" in date_str:
            parts = date_str.split("T")
            date_val = parts[0]
            if len(parts) > 1 and parts[1]:
                time_val = f"{parts[1]}:00" if len(parts[1]) == 5 else parts[1]

        # 1. СТЪПКА: Първо осигуряваме ТЕАТЪР, защото ни трябва веднага за пиесата!
        first_theatre = Theatre.objects.first()
        if not first_theatre:
            first_theatre = Theatre.objects.create(name="Народен театър")

        # 2. СТЪПКА: Създаваме PLAY, като му даваме времетраене И ТЕАТЪР (Решаваме новата грешка!)
        new_play = Play.objects.create(
            title=title,
            duration_minutes=120,
            theatre=first_theatre  # <-- Закачаме театъра към пиесата тук!
        )
        if hasattr(new_play, 'description'):
            new_play.description = description
            new_play.save()

        # 3. СТЪПКА: Осигуряваме ЗАЛА, обвързана с театъра
        first_hall = Hall.objects.first()
        if not first_hall:
            first_hall = Hall.objects.create(
                name="Главна зала", 
                capacity=100, 
                theatre=first_theatre
            )

        # 4. СТЪПКА: Създаваме ПРЕДСТАВЛЕНИЕ (Performance)
        p = Performance()
        p.play = new_play
        p.hall = first_hall
        
        if hasattr(p, 'title'): p.title = title
        if hasattr(p, 'description'): p.description = description

        # Записваме датата и часа
        if hasattr(p, 'date'): p.date = date_val
        elif hasattr(p, 'start_time'): p.start_time = date_val

        if hasattr(p, 'time'): 
            p.time = time_val

        # Записваме цената
        if hasattr(p, 'price'): 
            p.price = price

        # Запазваме всичко в базата
        p.save()

        return Response({
            "success": True,
            "message": "Всичко е навързано и записано успешно!",
            "id": p.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("!!! КРИТИЧНА ГРЕШКА В ТЕРМИНАЛА !!!:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    path('plays/', temporary_create_play, name='create_play'),
]