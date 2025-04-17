from django.db import models


class DistrictWeatherData(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    pm10 = models.FloatField(null=True, blank=True)
    pm2_5 = models.FloatField(null=True, blank=True)
    avg_temp = models.FloatField(null=True, blank=True)
    avg_pm2_5 = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["avg_temp", "avg_pm2_5"]

    def __str__(self):
        return self.name
