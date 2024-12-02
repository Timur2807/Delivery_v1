"""
В этом модуле представлены ссылки для представлений записей из БД.
"""

from django.urls import path, include

from my_app.views import (
    DeliveryAPIView,
    DeliveryModelViewSet,
    DeliveryStatus,
    CheckAddress,
)

app_name = 'my_app'

urlpatterns = [
    path('api/get/', DeliveryAPIView.as_view(), name='get'),

    path('api/get/<int:pk>/', DeliveryAPIView.as_view(), name='update'),
    path('api/get_status/<int:pk>/', DeliveryStatus.as_view(), name='get_status'),
    path('check_address/', CheckAddress.as_view(), name='check-address'),
]


