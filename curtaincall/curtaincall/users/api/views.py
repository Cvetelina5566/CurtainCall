# curtaincall/users/api/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from curtaincall.users.models import User


@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    email = data.get("email")
    password1 = data.get("password1")
    password2 = data.get("password2")

    if not email or not password1 or not password2:
        return JsonResponse({"detail": "Missing fields"}, status=400)

    if password1 != password2:
        return JsonResponse({"detail": "Passwords do not match"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"detail": "User already exists"}, status=400)

    user = User.objects.create_user(email=email, password=password1)

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email") or data.get("login")
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
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    email = data.get("email") or data.get("login")
    password = data.get("password")

    user = authenticate(request, email=email, password=password)

    if not user:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })
