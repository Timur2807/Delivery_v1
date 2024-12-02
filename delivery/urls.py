"""
URL configuration for delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from my_app.views import (
    DeliveryAPIView,
    DeliveryModelViewSet,
    DeliveryStatus,
    CheckAddress,
)


router = DefaultRouter()
router.register('orders', DeliveryModelViewSet)
urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api_list/', include(router.urls)), # подключение ModelViewSet
    path('', include('my_app.urls')),# подключаем урлы приложения my_app.urls
    # path('check/', CheckAddress.as_view()),# Простейшее подключение сервиса dadata для проверки адресов
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # подключение схемы документации.
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    # подключение swagger.
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # подключение redoc.
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns