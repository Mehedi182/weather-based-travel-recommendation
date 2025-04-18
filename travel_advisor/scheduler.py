import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command
from django.utils import timezone

logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=run_load_districts,
        trigger=CronTrigger(hour=0, minute=0, timezone=timezone.get_current_timezone()),
        id="load_districts_job",
        name="Load district weather and air data",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started: load_districts job will run at 12:00 AM daily")


def run_load_districts():
    try:
        call_command("load_districts")
        logger.info("Successfully ran load_districts command.")
    except Exception as e:
        logger.error(f"Error running load_districts: {e}")
