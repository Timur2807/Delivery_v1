"""
В этом модуле представлена джанго команда, которая запрашивает данные из БД.
"""
from django.core.management import BaseCommand
from django.db.models import Count, Avg, F, DurationField
from django.db.models.functions import ExtractHour, ExtractMinute
from datetime import timedelta

from my_app.models import *

class Command(BaseCommand):
    """
    3. Среднее время нахождение заявки на каждом этапе в городе Казань
    в разрезе типа посылки для завершенных заявок.
    """
    def handle(self, *args, **options):
        completed_deliveries = Delivery.objects.filter(
            delivery_city='Казань'
        ).annotate(last_status=F('deliverystatuscurrent__status_name')) # Получаем статус, который был завершен

        # Получаем историю статусов для завершенных заявок
        status_history = DeliveryStatusHistory.objects.filter(
            delivery__in=completed_deliveries,
            status_name__in=['Done', 'Cancelled']  # Учитываем только завершенные статусы
        )

        # Теперь мы можем сгруппировать данные по типу посылки и статусу
        average_times = status_history.values(
            'delivery__package_type',
            'status_name'
        ).annotate(
            average_duration=Avg(
                F('load_data') - F('delivery__load_data'),
                output_field=DurationField()
            )
        )
        for entry in average_times:
            self.stdout.write(
                f"Тип посылки: {entry['delivery__package_type']}, "
                f"Статус: {entry['status_name']}, "
                f"Среднее время: {entry['average_duration']}"
            )
        self.stdout.write(self.style.SUCCESS("Показал все"))