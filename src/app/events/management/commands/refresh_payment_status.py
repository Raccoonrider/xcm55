from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from events.models import ApplicationOrder

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        orders = (
            ApplicationOrder.objects.filter(
                payment_confirmed=False,
                saved__gte=(datetime.now() - timedelta(minutes=20))
            )
        )

        for order in orders:
            order.get_payment_result()
