from django.contrib import admin
from django.urls import path
from .views import BestDistrictsView, TravelRecommendationView, HealthCheckView

urlpatterns = [
    path("best-districts/", BestDistrictsView.as_view(), name="best-districts"),
    path(
        "travel-recommendation/",
        TravelRecommendationView.as_view(),
        name="travel-recommendation",
    ),
    path("health/", HealthCheckView.as_view(), name="health_check"),
]
