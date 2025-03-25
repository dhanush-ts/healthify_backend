from rest_framework.views import APIView
from rest_framework.response import Response
from user_model.authentication import IsAuthenticated
from .models import DailyConsumption
from datetime import timedelta
from .serializer import DailyConsumptionSerializer
from django.utils.timezone import now

class DailyConsumptionView(APIView):
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        """Fetches the logged-in user's daily consumption."""
        user = request.user
        today = now().date()
        consumption, created = DailyConsumption.objects.get_or_create(user=user, date=today)  # Default to 0 if no data exists

        serializer = DailyConsumptionSerializer(consumption)
        return Response(serializer.data)

    def post(self, request):
        """Updates the user's daily consumption."""
        user = request.user
        today = now().date()

        consumption, created = DailyConsumption.objects.get_or_create(user=user, date=today)
        serializer = DailyConsumptionSerializer(consumption, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class WeeklyConsumption(APIView):
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        start_date = today - timedelta(days=today.weekday())  # Monday of the current week
        end_date = start_date + timedelta(days=6)  # Sunday of the current week

        weekly_consumption = DailyConsumption.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        )

        serializer = DailyConsumptionSerializer(weekly_consumption, many=True)
        return Response({"consumption": serializer.data})