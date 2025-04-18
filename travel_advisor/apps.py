from django.apps import AppConfig


class TravelAdvisorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "travel_advisor"

    def ready(self):
        from . import scheduler

        scheduler.start()
