from ..models import Performance
from django.shortcuts import get_object_or_404

def get_all_performances():
    """
    Returns all performances with related play, hall, and theatre data
    Optimized with select_related
    """
    return (
        Performance.objects
        .select_related(
            "play",
            "hall",
            "hall__theatre",
            "play__theatre",
        )
        .all()
        .order_by("date", "time")
    )

def get_performance_by_id(performance_id: int):
    """
    Returns a single performance by ID with related data
    Optimized with select_related
    """
    return get_object_or_404(
        Performance.objects.select_related(
            "play",
            "hall",
            "hall__theatre",
            "play__theatre",
        ),
        id=performance_id
    )
