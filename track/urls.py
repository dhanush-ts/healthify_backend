from django.urls import path
from .views import DailyConsumptionView, WeeklyConsumption

urlpatterns = [
    path('daily-consumption/', DailyConsumptionView.as_view(), name='consumption-daily'),
    path('weekly-consumption/', WeeklyConsumption.as_view(), name='consumption-weekly'),
]