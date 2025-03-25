from rest_framework import serializers
from .models import TrackableItem, DailyConsumption


class TrackableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackableItem
        fields = ['id', 'name']


class DailyConsumptionSerializer(serializers.ModelSerializer):
    track_item_name = serializers.ReadOnlyField(source="track_item.name")  # Show item name in response

    class Meta:
        model = DailyConsumption
        fields = ['id', 'track_item', 'track_item_name', 'date', 'units']
