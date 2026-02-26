# theatres/models/order.py
from django.db import models

class Order(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
