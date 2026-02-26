from django.db import models
from .hall import Hall

class Seat(models.Model):
    row = models.CharField(max_length=5)
    number = models.IntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")

    class Meta:
        unique_together = ('row', 'number', 'hall')

    def __str__(self):
        return f"{self.row}{self.number} ({self.hall.name})"
