"""
В этом модуле представлена джанго команда, которая запрашивает данные из БД.
"""

import datetime

from django.core.management import BaseCommand
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from my_app.models import *


class Command(BaseCommand):
    """
    2. Количество заявок в разрезе статусов,
    которые поступили за последние 3 недели с типом доставки «Письмо» и «Бандероль».
    """
    def handle(self, *args, **options):
        self.stdout.write("start process")
        status_counts = (
            DeliveryStatusCurrent.objects.filter(
                delivery__delivery_date__range=(datetime.datetime(2024, 7, 19), datetime.datetime(2024, 9, 8)),
                delivery__package_type__in=['Письмо', 'Бандероль']
            ).values('status_name').annotate(count=Count('id')).order_by('status_name')
        )
        for status in status_counts:
            self.stdout.write(f"Статус: {status['status_name']}, Количество: {status['count']}")
        self.stdout.write(self.style.SUCCESS("The end process"))