import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password") or request.data.get("password1")

        if not email or not password:
            return Response({"error": "Имейл и парола са задължителни!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Потребител с този имейл вече съществува."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        
        return Response({
            "success": True, 
            "message": "Регистрацията е успешна!"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"Вътрешна грешка: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
    except Exception:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    if not email or not password:
        return JsonResponse({"detail": "Missing email or password"}, status=400)

    user = authenticate(request, email=email, password=password)

    if not user:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "token": str(refresh.access_token), 
        "is_pr": user.is_staff,            
    })