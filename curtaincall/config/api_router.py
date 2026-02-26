from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from curtaincall.users.api.views import login_user

from curtaincall.users.api.views import register_user, login_user

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# router.register("users", UserViewSet)


# app_name = "api"
urlpatterns = router.urls + [
    path("register/", register_user, name="api-register"),
    path("login/", login_user, name="api-login"),
]
