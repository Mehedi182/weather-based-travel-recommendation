import logging
from datetime import date, timedelta

from django.db import connection
from django.db.models import Avg
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DistrictWeatherData
from .serializers import BestDistrictsSerializer

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HealthCheckView(APIView):
    def get(self, request):
        try:
            connection.ensure_connection()
            logger.info("Health check passed")
            return JsonResponse({"status": "healthy"}, status=200)
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)


class BestDistrictsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        logger.info("Fetching best districts for travel")
        try:
            date_threshold = date.today() - timedelta(days=7)
            districts = (
                DistrictWeatherData.objects.filter(date__gte=date_threshold)
                .values("name")
                .annotate(avg_temp=Avg("temperature"), avg_pm2_5=Avg("pm2_5"))
                .order_by("avg_temp", "avg_pm2_5")[:10]
            )

            logger.info(f"Found {len(districts)} districts")
            serializer = BestDistrictsSerializer(districts, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching best districts: {e}")
            return Response(
                {"error": "An error occurred while fetching best districts"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TravelRecommendationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        logger.info("Processing travel recommendation request")
        current_lat = request.data.get("current_latitude")
        current_lon = request.data.get("current_longitude")
        destination_district = request.data.get("destination_district")
        travel_date = request.data.get("travel_date")

        if not all([current_lat, current_lon, destination_district, travel_date]):
            logger.warning("Missing required parameters in request")
            return Response(
                {"error": "Missing required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            logger.info(f"Fetching data for destination: {destination_district}")
            dest_data = DistrictWeatherData.objects.filter(
                name__iexact=destination_district, date=travel_date
            ).first()

            if not dest_data:
                logger.warning(
                    f"No data available for destination {destination_district} on {travel_date}"
                )
                return Response(
                    {"error": "No data available for destination on this date"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            logger.info("Fetching data for current location")
            current_data = DistrictWeatherData.objects.filter(
                latitude=current_lat, longitude=current_lon, date=travel_date
            ).first()

            if not current_data:
                logger.warning(
                    f"No data available for current location ({current_lat}, {current_lon}) on {travel_date}"
                )
                return Response(
                    {"error": "No data available for your current location"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            temp_diff = (dest_data.temperature or 0) - (
                current_data.temperature or 0
            )  # wheater api return null values for some of the days. thats why considering 0
            pm25_diff = (dest_data.pm2_5 or 0) - (current_data.pm2_5 or 0)
            logger.info(
                f"Temperature difference: {temp_diff}, PM2.5 difference: {pm25_diff}"
            )

            recommendation, reason = self.generate_recommendation(temp_diff, pm25_diff)
            logger.info(f"Recommendation: {recommendation}, Reason: {reason}")

            return Response(
                {
                    "recommendation": recommendation,
                    "reason": reason,
                    "comparison": {
                        "temperature": {
                            "current": current_data.temperature,
                            "destination": dest_data.temperature,
                            "difference": round(temp_diff, 1),
                        },
                        "air_quality": {
                            "current": current_data.pm2_5,
                            "destination": dest_data.pm2_5,
                            "difference": round(pm25_diff, 1),
                        },
                    },
                }
            )

        except Exception as e:
            logger.error(f"Error processing travel recommendation: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def generate_recommendation(self, temp_diff, pm25_diff):
        if temp_diff < 0 and pm25_diff < 0:
            recommendation = "Recommended"
            reason = f"Your destination is {abs(round(temp_diff, 1))}°C cooler and has significantly better air quality. Enjoy your trip!"
        else:
            recommendation = "Not Recommended"
            reason = "Your destination is hotter and has worse air quality than your current location. It’s better to stay where you are."

        logger.info(f"Generated recommendation: {recommendation}, Reason: {reason}")
        return recommendation, reason
