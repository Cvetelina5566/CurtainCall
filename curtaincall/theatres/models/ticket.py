from django.db import models
from .performance import Performance
from .seat import Seat

class Ticket(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="tickets")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="tickets")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_sold = models.BooleanField(default=False)

    class Meta:
        unique_together = ('performance', 'seat')

    def __str__(self):
        return f"Ticket for {self.performance} – Seat {self.seat}"
