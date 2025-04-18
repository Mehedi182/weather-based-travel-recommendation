from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import DistrictWeatherData
from .views import TravelRecommendationView


class WeatherRecommendationTests(APITestCase):
    def setUp(self):
        self.district_1 = DistrictWeatherData.objects.create(
            name="District A",
            date=date.today(),
            temperature=25.0,
            pm2_5=30.0,
            latitude=23.8103,
            longitude=90.4125,
        )

        self.district_2 = DistrictWeatherData.objects.create(
            name="District B",
            date=date.today(),
            temperature=20.0,
            pm2_5=10.0,
            latitude=24.0000,
            longitude=91.0000,
        )

        self.old_district = DistrictWeatherData.objects.create(
            name="District C",
            date=date.today() - timedelta(days=10),
            temperature=22.0,
            pm2_5=25.0,
            latitude=25.0000,
            longitude=89.0000,
        )
        self.view = TravelRecommendationView()

    def test_best_districts_view(self):
        url = reverse("best-districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertIn("name", response.data[0])

    def test_travel_recommendation_view_success(self):
        url = reverse("travel-recommendation")
        data = {
            "current_latitude": 23.8103,
            "current_longitude": 90.4125,
            "destination_district": "District B",
            "travel_date": str(date.today()),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("recommendation", response.data)
        self.assertIn("comparison", response.data)

    def test_travel_recommendation_missing_params(self):
        url = reverse("travel-recommendation")
        data = {
            "current_latitude": 23.8103,
            "travel_date": str(date.today()),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_travel_recommendation_no_destination_data(self):
        url = reverse("travel-recommendation")
        data = {
            "current_latitude": 23.8103,
            "current_longitude": 90.4125,
            "destination_district": "NonExistent",
            "travel_date": str(date.today()),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recommendation_good_conditions(self):
        recommendation, reason = self.view.generate_recommendation(
            temp_diff=-3, pm25_diff=-15
        )
        self.assertEqual(recommendation, "Recommended")
        self.assertIn("cooler", reason)
        self.assertIn("better air quality", reason)

    def test_recommendation_bad_conditions(self):
        recommendation, reason = self.view.generate_recommendation(
            temp_diff=5, pm25_diff=10
        )
        self.assertEqual(recommendation, "Not Recommended")
        self.assertIn("hotter", reason.lower())

    def test_travel_recommendation_no_current_data(self):
        url = reverse("travel-recommendation")
        data = {
            "current_latitude": 20.0000,
            "current_longitude": 20.0000,
            "destination_district": "District B",
            "travel_date": str(date.today()),
        }
        print(data)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
