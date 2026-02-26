from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="accounts/register.html"),
        name="home",
    ),

    path("admin/", admin.site.urls),

    # ADD THIS ↓↓↓↓↓
    # path("auth/", include("allauth.urls")),
    # ---------

    # HEADLESS API
    path("auth/", include("allauth.headless.urls")),  # включва /auth/register/ и /auth/login/

    path("api/", include("theatres.urls")),

    path("api/jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("api/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    
    #path("accounts/", include("allauth.urls")),

    path("api/", include("config.api_router")),
]

# Static/Media (ако има)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
