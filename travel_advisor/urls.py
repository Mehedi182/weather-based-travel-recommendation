from django.contrib import admin
from django.urls import path
from .views import BestDistrictsView, TravelRecommendationView

urlpatterns = [
    path("best-districts/", BestDistrictsView.as_view(), name="best-districts"),
    path(
        "travel-recommendation/",
        TravelRecommendationView.as_view(),
        name="travel-recommendation",
    ),
]
