from rest_framework import generics
from user_model.authentication import IsAuthenticated
from django.utils.timezone import now
from .models import TrackableItem, DailyConsumption
from .serializer import TrackableItemSerializer, DailyConsumptionSerializer
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import re
import PyPDF2
from django.http import JsonResponse

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
    - GET: If no records exist, return all registered track items with units = 0.
    - POST: If an entry for track_type exists on the same date, update it instead of creating a new one.
    """
    serializer_class = DailyConsumptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve today's consumption records for the authenticated user."""
        today = now().date()
        queryset = DailyConsumption.objects.filter(user=self.request.user, date=today)

        if not queryset.exists():
            # If no records exist, return all trackable items with 0 consumption
            track_types = ["Alcohol", "Cigarettes", "Caffeine", "Sugar"]  # Modify as needed
            return [DailyConsumption(user=self.request.user, date=today, track_type=track, units=0) for track in track_types]

        return queryset

    def list(self, request, *args, **kwargs):
        """Handle GET requests and return data properly formatted."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Allow updating the same day's records instead of creating new ones."""
        today = now().date()
        track_type = self.request.data.get("track_type")

        # Check if an entry already exists for the user, track_type, and today
        existing_entry = DailyConsumption.objects.filter(
            user=self.request.user, date=today, track_type=track_type
        ).first()

        if existing_entry:
            # Update existing record
            existing_entry.units = self.request.data.get("units", existing_entry.units)
            existing_entry.save()
            return Response(DailyConsumptionSerializer(existing_entry).data)
        else:
            # Create a new record
            serializer.save(user=self.request.user, date=today)


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

class ExtractMedicalReportView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Ensure file is provided
        if 'pdf' not in request.FILES:
            return JsonResponse({"error": "No PDF file uploaded"}, status=400)

        pdf_file = request.FILES['pdf']
        extracted_text = self.extract_text_from_pdf(pdf_file)

        # Extract fields using regex
        extracted_data = self.extract_fields(extracted_text)

        return JsonResponse(extracted_data, status=200)

    def extract_text_from_pdf(self, pdf_file):
        """Extracts text from a given PDF file."""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            return f"Error reading PDF: {e}"
        return text

    def extract_fields(self, text):
        """Extracts relevant fields using regex patterns."""
        patterns = {
            "full_name": r"Name:\s*(.+)",
            "phone_number": r"Phone Number:\s*(\d{10})",
            "dob": r"Date of Birth:\s*(\d{2}/\d{2}/\d{4})",
            "gender": r"Gender:\s*(Male|Female|Other)",
            "height": r"Height:\s*(\d+\s*cm)",
            "weight": r"Weight:\s*(\d+\s*kg)",
            "city": r"City:\s*(.+)",
            "medical_history": r"Past Conditions:\s*(.+)",
            "genetic_predisposition": r"Family History:\s*(.+)",
            "smoking": r"Smoking:\s*(Yes|No|Occasionally|.+)",
            "drinking": r"Drinking:\s*(Yes|No|Occasionally|.+)",
            "sleeping_hours": r"Sleeping Hours:\s*(\d+)",
            "exercise_hours": r"Exercise Hours:\s*(\d+)",
        }

        extracted_data = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            extracted_data[key] = match.group(1).strip() if match else None

        return extracted_data