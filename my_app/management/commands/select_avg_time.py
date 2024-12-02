from django.core.management import BaseCommand
from django.db.models import Count, Avg, F, DurationField
from django.db.models.functions import ExtractHour, ExtractMinute
from datetime import timedelta

from my_app.models import *

class Command(BaseCommand):
    """
    1. Количество успешно завершенных заказов
    И их среднее время выполнения в разрезе городов.
    """
    def handle(self, *args, **options):
        self.stdout.write("select all objects")
        completed_orders = DeliveryStatusCurrent.objects.filter(status_name='Done')
        results = (
            completed_orders
            .values('delivery__delivery_city')  # Группируем по городу
            .annotate(
                completed_count=Count('id'),  # Количество завершенных заказов
                average_duration=Avg(
                    ExtractHour(F('load_data')) * 60 + ExtractMinute(F('load_data')),
                    output_field=DurationField()
                )  # Среднее время выполнения
            )
        )
        summary = []
        for result in results:
            city = result['delivery__delivery_city']
            count = result['completed_count']

            # Преобразуем avg_duration_minutes в целое число
            avg_duration_minutes = int(result['average_duration']) if result['average_duration'] else 0

            # Создаем timedelta с целым числом
            avg_duration = str(timedelta(minutes=avg_duration_minutes))

            summary.append(
                {
                    'city': city,
                    'completed_count': count,
                    'average_duration': avg_duration
                }
            )
        self.stdout.write(f"{summary}")
        self.stdout.write(self.style.SUCCESS("Показал все"))