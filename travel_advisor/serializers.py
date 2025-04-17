from rest_framework import serializers
from .models import DistrictWeatherData


class DistrictWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictWeatherData
        fields = [
            "id",
            "name",
            "date",
            "latitude",
            "longitude",
            "temperature",
            "pm10",
            "pm2_5",
            "avg_temp",
            "avg_pm2_5",
        ]


class BestDistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictWeatherData
        fields = ["name", "avg_temp", "avg_pm2_5"]
