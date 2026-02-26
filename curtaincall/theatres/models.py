from django.db import models
from django.contrib.auth.models import User


class Play(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заглавие")
    description = models.TextField(verbose_name="Описание на сюжета")

    def __str__(self):
        return self.title

class Hall(models.Model):
    name = models.CharField(max_length=100, verbose_name="Име на зала")
    capacity = models.PositiveIntegerField(verbose_name="Капацитет (места)")

    def __str__(self):
        return self.name

class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name="Пиеса")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name="Зала")
    date_time = models.DateTimeField(verbose_name="Дата и час")

    def __str__(self):
        return f"{self.play.title} - {self.date_time.strftime('%m.%d.%Y %H:%M')}"
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Потребител")
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, verbose_name="Представление")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Брой билети")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата на закупуване")

    def __str__(self):
        return f"{self.user.username} - {self.quantity} бр. за {self.performance.play.title}"