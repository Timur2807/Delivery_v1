from django.contrib import admin
from .models import *
# Register your models here.

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'delivery_city', 'package_type')
    list_display_links = ('id', 'customer_name')
    search_fields = ('id', 'customer_name', 'delivery_address')
    ordering = ('-load_data',)


admin.site.register(Delivery, DeliveryAdmin)


class DeliveryStatusCurrentAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name', 'load_data')
    list_display_links = ('id', 'status_name')
    search_fields = ('id', 'status_name', 'load_data')
    ordering = ('-load_data',)


admin.site.register(DeliveryStatusCurrent, DeliveryStatusCurrentAdmin)


class DeliveryStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_id', 'status_name', 'load_data')
    list_display_links = ('id', 'delivery_id', 'status_name')
    search_fields = ('id', 'delivery_id', 'status_name', 'load_data')
    ordering = ('-load_data',)


admin.site.register(DeliveryStatusHistory, DeliveryStatusHistoryAdmin)
