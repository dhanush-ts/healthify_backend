from django.db import models
from user_model.models import User
from django.utils import timezone

class TrackableItem(models.Model):
    """Things the user wants to track (e.g., Cigarettes, Alcohol, Coffee)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trackable_items")
    name = models.CharField(max_length=100)  # e.g., Cigarettes, Alcohol

    def __str__(self):
        return f"{self.name} (Tracked by {self.user.full_name})"


class DailyConsumption(models.Model):
    """Tracks user consumption per day."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_consumption")
    track_item = models.ForeignKey(TrackableItem, on_delete=models.CASCADE, related_name="consumption_records")
    date = models.DateField(default=timezone.now)  # Daily tracking
    units = models.PositiveIntegerField(default=0)  # Default 0 if no data is provided

    class Meta:
        unique_together = ('user', 'track_item', 'date')  # Ensures unique daily entry per tracked item

    def __str__(self):
        return f"{self.user.full_name} - {self.track_item.name} on {self.date}: {self.units} units"
