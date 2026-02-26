from django.db import models
from .theatre import Theatre

class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField()
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="plays")

    def __str__(self):
        return self.title
