from rest_framework import serializers

from .models import DistrictWeatherData


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictWeatherData
        fields = ["id", "name", "latitude", "longitude", "avg_temperature", "avg_pm25"]
