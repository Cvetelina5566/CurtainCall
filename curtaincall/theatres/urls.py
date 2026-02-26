from django.urls import path

from .views import buy_ticket
from .views.performance import PerformanceListAPIView, PerformanceDetailAPIView
from .views.pr import TheatreListAPIView, PlayListAPIView, HallListAPIView
from . import views

urlpatterns = [
    path("performances/", PerformanceListAPIView.as_view(), name="performance-list"),
    path("performances/<int:pk>/", PerformanceDetailAPIView.as_view(), name="performance-detail"),
    # PR endpoints
    path("theatres/", TheatreListAPIView.as_view(), name="theatre-list"),
    path("plays/", PlayListAPIView.as_view(), name="play-list"),
    path("halls/", HallListAPIView.as_view(), name="hall-list"),
    path('tickets/buy/', buy_ticket, name='buy_ticket'),
]
