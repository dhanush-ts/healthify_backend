from django.urls import path
from .views import TrackableItemListCreateView, DailyConsumptionListCreateView, WeeklyConsumptionView, ExtractMedicalReportView

urlpatterns = [
    path('trackable-items/', TrackableItemListCreateView.as_view(), name="trackable-items"),
    path('daily-consumption/', DailyConsumptionListCreateView.as_view(), name="daily-consumption"),
    path('weekly-consumption/', WeeklyConsumptionView.as_view(), name="weekly-consumption"),
    path('extract-medical-report/', ExtractMedicalReportView.as_view(), name="extract-medical-report"),
]
