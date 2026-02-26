from django.db import models
from .order import Order
from .ticket import Ticket

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name="order_item")

    def __str__(self):
        return f"OrderItem: Ticket {self.ticket.id} in Order {self.order.id}"
