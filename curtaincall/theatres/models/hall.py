from django.db import models
from .theatre import Theatre

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="halls")

    def __str__(self):
        return f"{self.name} – {self.theatre.name}"
