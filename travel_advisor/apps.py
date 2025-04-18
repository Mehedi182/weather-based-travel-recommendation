import sys

from django.apps import AppConfig


class TravelAdvisorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "travel_advisor"

    def ready(self):
        # Avoid running when doing migrations or other manage.py commands
        if "runserver" in sys.argv:
            from travel_advisor.scheduler import start  # Only import if needed

            start()
