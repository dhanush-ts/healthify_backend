from rest_framework import serializers
from .models import DailyConsumption

class DailyConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyConsumption
        fields = ['date', 'cigarettes_smoked', 'alcohol_units']
