from rest_framework import generics
from user_model.authentication import IsAuthenticated
from django.utils.timezone import now
from .models import TrackableItem, DailyConsumption
from .serializer import TrackableItemSerializer, DailyConsumptionSerializer
from datetime import timedelta


class TrackableItemListCreateView(generics.ListCreateAPIView):
    """
    Users can create and list their trackable items (e.g., Cigarettes, Alcohol, Coffee).
    """
    serializer_class = TrackableItemSerializer
    authentication_classes = [IsAuthenticated]

    def get_queryset(self):
        return TrackableItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyConsumptionListCreateView(generics.ListCreateAPIView):
    """
    Users can log their daily consumption and retrieve their consumption history.
    """
    serializer_class = DailyConsumptionSerializer
    authentication_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyConsumption.objects.filter(user=self.request.user, date=now().date())

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WeeklyConsumptionView(generics.ListAPIView):
    """
    Retrieves the logged-in user's weekly consumption.
    """
    serializer_class = DailyConsumptionSerializer
    authentication_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
        return DailyConsumption.objects.filter(user=user, date__gte=start_of_week).order_by('-date')
