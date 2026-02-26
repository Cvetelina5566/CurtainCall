from django.db import models
from .play import Play
from .hall import Hall

class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="performances")
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('play', 'hall', 'date', 'time')

    def __str__(self):
        return f"{self.play.title} @ {self.date} {self.time}"
