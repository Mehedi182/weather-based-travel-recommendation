from django.contrib import admin

from .models import DistrictWeatherData


@admin.register(DistrictWeatherData)
class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date",
        "latitude",
        "longitude",
        "temperature",
        "pm10",
        "pm2_5",
        "avg_temp",
        "avg_pm2_5",
        "last_updated",
    )
    search_fields = ("name",)
    list_filter = ("date",)
    ordering = ("-date",)