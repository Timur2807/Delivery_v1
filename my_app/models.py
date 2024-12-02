from django.db import models

class Delivery(models.Model):
    PACKAGE = [
        (None, 'Выберите тип пакета'),
        ('letter', 'Письмо'),
        ('parcel', 'Бандероль'),
        ('bulky cargo', 'Крупногабаритный груз'),
    ]
    load_data = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=150)
    delivery_city = models.CharField(max_length=150)
    delivery_address = models.CharField(max_length=250)
    delivery_date = models.DateField(auto_now_add=True)
    delivery_time = models.TimeField(auto_now_add=True)
    package_type = models.CharField(choices=PACKAGE)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}, {self.customer_name} - {self.delivery_city}, {self.package_type}, {self.delivery_date}, {self.delivery_time}'

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ['-load_data']

class DeliveryStatusCurrent(models.Model):
    PACKAGE_STATUS = [
        (None, 'Выберите статус'),
        ('New', 'Новая'),
        ('Done', 'Завершенная'),
        ('Cancelled', 'Закрытая'),
        ('Handed to courier', 'Передано курьеру'),
        ('In process', 'В процессе'),
    ]

    status_name = models.CharField(choices=PACKAGE_STATUS, blank=True, null=True)
    load_data = models.DateTimeField(auto_now_add=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.id}, {self.status_name} - {self.load_data}'

    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'
        ordering = ['-load_data']

class DeliveryStatusHistory(models.Model):
    PACKAGE_STATUS = [
        (None, 'Выберите статус'),
        ('New', 'Новая'),
        ('Done', 'Завершенная'),
        ('Canceled', 'Закрытая'),
        ('Handed to courier', 'Передано курьеру'),
        ('In process', 'В процессе'),
    ]
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, blank=True, null=True)
    status_name = models.CharField(choices=PACKAGE_STATUS, blank=True, null=True)
    load_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.delivery}, {self.status_name} - {self.load_data}'

    class Meta:
        verbose_name = 'История доставки'
        verbose_name_plural = 'История доставок'
        ordering = ['-load_data']


class Warehouse(models.Model):
    """
    Класс для описания склада для доставки.
    """
    city = models.CharField('Город', max_length=150, db_index=True)
    address = models.CharField('Адрес склада', max_length=250)

    def __str__(self):
        return f'{self.city}, {self.address}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'