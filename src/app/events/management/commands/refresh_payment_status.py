from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from events.models import Application

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        applications = (
            Application.objects.filter(
                payment_confirmed=False,
                saved__gte=(datetime.now() - timedelta(minutes=20))
            )
        )

        for application in applications:
            application.get_payment_result()
