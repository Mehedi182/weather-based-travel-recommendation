import json
import os
from typing import Dict

import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now, timedelta
from retry_requests import retry

from travel_advisor.models import DistrictWeatherData


def get_openmeteo_client(
    expire_after: int = 3600, retries: int = 5, backoff_factor: float = 0.2
):
    cache_session = requests_cache.CachedSession(".cache", expire_after=expire_after)
    retry_session = retry(cache_session, retries=retries, backoff_factor=backoff_factor)
    return openmeteo_requests.Client(session=retry_session)


def fetch_weather_data(client, latitude: float, longitude: float) -> pd.DataFrame:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "timezone": "Asia/Dhaka",
    }
    response = client.weather_api(url, params=params)[0]

    # print(f"Coordinates: {response.Latitude()}°N, {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"UTC Offset: {response.UtcOffsetSeconds()} s")

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left",
    )

    df = pd.DataFrame(
        {
            "date": dates,
            "temperature": hourly_temperature_2m,
        }
    )

    return df


def fetch_air_quality_data(client, latitude: float, longitude: float) -> pd.DataFrame:
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["pm10", "pm2_5"],
        "timezone": "Asia/Dhaka",
        "forecast_days": 7,
    }
    response = client.weather_api(url, params=params)[0]

    hourly = response.Hourly()
    hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
    hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()

    dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left",
    )

    df = pd.DataFrame(
        {
            "date": dates,
            "pm10": hourly_pm10,
            "pm2_5": hourly_pm2_5,
        }
    )

    return df


def filter_2pm_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["date"].dt.hour == 14]
    return df


def get_weather_and_air_quality(
    latitude: float,
    longitude: float,
    expire_after: int = 3600,
    retries: int = 5,
    backoff_factor: float = 0.2,
) -> Dict[str, pd.DataFrame]:
    client = get_openmeteo_client(expire_after, retries, backoff_factor)

    weather_df = fetch_weather_data(client, latitude, longitude)
    air_quality_df = fetch_air_quality_data(client, latitude, longitude)

    filtered_weather_df = filter_2pm_data(weather_df)
    filtered_air_quality_df = filter_2pm_data(air_quality_df)

    merged_df = pd.merge(
        filtered_weather_df, filtered_air_quality_df, on="date", how="inner"
    )
    avg_tmp = merged_df["temperature"].mean()
    avg_pm_2_5 = merged_df["pm2_5"].mean()
    merged_df["avg_temp"] = avg_tmp
    merged_df["avg_pm2_5"] = avg_pm_2_5
    return merged_df


def district_wise_data() -> pd.DataFrame:
    file_path = os.path.join(os.path.dirname(__file__), "bd_districts.json")
    with open(file_path, "r") as file:
        bd_districts = json.load(file)
    dfs = []
    for district in bd_districts["districts"]:
        latitude = district["lat"]
        longitude = district["long"]
        district_name = district["name"]
        print(
            f"Fetching and loading data for {district_name} (Lat: {latitude}, Long: {longitude})"
        )

        try:
            weather_and_air_quality_data = get_weather_and_air_quality(
                latitude, longitude
            )
            weather_and_air_quality_data["name"] = district_name
            weather_and_air_quality_data["latitude"] = latitude
            weather_and_air_quality_data["longitude"] = longitude
            dfs += [weather_and_air_quality_data]
        except Exception as e:
            print(f"Failed to fetch data for {district_name}: {e}")
    return dfs


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Delete data from the last 7 days
        seven_days_ago = now() - timedelta(days=7)
        DistrictWeatherData.objects.filter(date__gte=seven_days_ago).delete()

        dfs = district_wise_data()
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            district_datas = [
                DistrictWeatherData(**row) for row in df.to_dict(orient="records")
            ]
        else:
            district_datas = []

        with transaction.atomic():
            DistrictWeatherData.objects.bulk_create(district_datas, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("Successfully loaded district data"))
