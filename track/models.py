from django.db import models
from user_model.models import User
from django.utils import timezone

class DailyConsumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_consumption")
    date = models.DateField(default=timezone.now, unique=True)  # Tracks daily records
    cigarettes_smoked = models.PositiveIntegerField(default=0)  # Default 0 if no data is provided
    alcohol_units = models.FloatField(default=0.0)  # Default 0 if no data is provided (1 unit = 10ml pure alcohol)

    class Meta:
        unique_together = ('user', 'date')  # Ensures one record per user per day

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.cigarettes_smoked} cigarettes, {self.alcohol_units} units"
