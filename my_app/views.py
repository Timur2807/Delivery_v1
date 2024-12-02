import dadata
from geopy.distance import great_circle
from rest_framework.filters import SearchFilter

from delivery.settings import DADATA_API_KEY, DADATA_SECRET_KEY
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


from .models import Delivery, DeliveryStatusCurrent, DeliveryStatusHistory, Warehouse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import DeliverySerializer, DeliveryStatusSerializer, DeliverySerializerSet
from .models import DeliveryStatusCurrent, DeliveryStatusHistory


class DeliveryAPIView(APIView):
    """
        Этот класс представляет собой представление на основе базового класса APIVIEW.
        Класс обрабатывает запросы как GET, POST, PUT, DELETE.

        Представляет таблицу заказов из БД.
    """
    def get(self, request):
        """
        Этот метод обрабатывает GET запрос.
        :param request:
        :return: все объекты из БД
        """
        order = Delivery.objects.all().values()
        return Response({'order': list(order)})

    def post(self, request):
        """
            Этот метод обрабатывает POST запрос.
            Так же создает новые записи в других таблицах БД.
        :param request:
        :return: id новой записи
        """
        order = Delivery.objects.create(
            customer_name=request.data['customer_name'],
            delivery_city=request.data['delivery_city'],
            delivery_address=request.data['delivery_address'],
            package_type=request.data['package_type'],
            comment=request.data['comment']
        )
        dct = model_to_dict(order)
        # ниже происходит создание новый записи в таблице статусов БД.
        current_status = DeliveryStatusCurrent(
            status_name='new',
            delivery_id=dct['id']
        )
        current_status.save()
        # ниже происходит создание новый записи в таблице истории БД.
        history_status = DeliveryStatusHistory(
            delivery_id=dct['id'],
            status_name='new',
        )
        history_status.save()

        return Response({'New_order': dct['id']})

    def put(self, request, *args, **kwargs):
        """
            Этот метод обрабатывает PUT запрос.
            Обновляет запись в таблице заказов.
        :param request:
        :param args:
        :param kwargs:
        :return: обновлённые поля из таблицы
        """
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Missing order ID'}, status=400)

        try:
            instance = Delivery.objects.get(pk=pk)
        except:
            return Response({'error': 'Missing order ID'}, status=400)

        serializer = DeliverySerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()

        return Response({'order_updated': serializer.data})

    def delete(self, request, *args, **kwargs):
        """
            Этот метод обрабатывает DELETE запрос.
            Удаляет запись в таблице заказов из БД.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Missing order ID'}, status=400)

        try:
            instance = Delivery.objects.get(pk=pk)
        except:
            return Response({'error': 'Missing order ID'}, status=400)

        instance.delete()
        return Response({'order_deleted': 'Order deleted successfully'})



class DeliveryStatus(APIView):
    """
        Этот класс представляет собой представление на основе базового класса APIVIEW.
        Класс обрабатывает запросы как GET, POST, PUT, DELETE.

        Представляет таблицу статус заказов из БД.
    """
    def get(self, request, pk):
        """
        Обрабатывает GET запрос.
        :param request:
        :param pk:
        :return: Статус конкретного заказа
        """
        status = DeliveryStatusCurrent.objects.get(pk=pk)
        return Response({f"Статус заказа № {pk}": status.status_name})

    def put(self, request, *args, **kwargs):
        """
        Обрабатывает PUT запрос.
        :param request:
        :param args:
        :param kwargs:
        :return: Измененный статус.
        """
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Don\'t found ID'}, status=400)

        try:
            instance = DeliveryStatusCurrent.objects.get(pk=pk)

        except:
            return Response({'error': 'Missing status ID'}, status=400)

        serializer = DeliveryStatusSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        history = DeliveryStatusHistory(
            delivery_id=instance.delivery_id,
            status_name=request.data['status_name']
        )
        history.save()

        return Response({
            'status_updated': serializer.data,
            'new_status_history': model_to_dict(history),
        })


def extract_city(address):
    """
    Метод принимает response['result'] из сервиса dadata и оттуда вытаскивает город
    :param address: str
    :return name city: str
    """
    address = address.strip()
    first_index = address.find("г")
    second_index = address.find(" ул")
    second_index_last = address.find("пр-кт")
    second_index_3 = address.find("б-р")
    if first_index != -1 and second_index != -1:
        city_name = address[first_index + 1:second_index].replace(',', '')
    elif first_index != -1 and second_index_last != -1:
        city_name = address[first_index + 1:second_index_last].replace(',', '')
    elif first_index != -1 and second_index_3 != -1:
        city_name = address[first_index + 1:second_index_3].replace(',', '')
    else:
        return f"Введите корректный адрес." \
               f"Пример г Казань ул Суворова, д.91а"
    return f"{city_name}"



class CheckAddress(APIView):
    """
    Класс обрабатывает GET запрос по валидации адресов со складами.
    """
    def get(self, request):
        try:
            query = request.GET.get('query')
            dadata_client = dadata.Dadata(DADATA_API_KEY, DADATA_SECRET_KEY)
            response = dadata_client.clean('address', query)
            cordin_1 = (response['geo_lat'], response['geo_lon'])
            city = extract_city(response['result']).strip()
            warehouse = Warehouse.objects.get(city=city)
            city_war = warehouse.city
            address_war = warehouse.address
            query_war = city_war + " " + address_war
            response_war = dadata_client.clean('address', query_war)
            cordin_2 = (response_war['geo_lat'], response_war['geo_lon'])
            distance = great_circle(cordin_1, cordin_2).km
            return Response({
                "Адрес доставки": response['result'],
                "Адрес склада": response_war['result'],
                "Дистанция": f"{distance:.2f}"
            }, status=status.HTTP_200_OK)
        except Warehouse.DoesNotExist:
            return Response({"error": "Warehouse not found"}, status=status.HTTP_404_NOT_FOUND)



class DeliveryModelViewSet(ModelViewSet):
    """
    Этот класс представляет собой представление на основе класса ModelViewSet.
    Класс обрабатывает запросы как GET, POST, PUT, DELETE.
    Класс представляет таблицу заказов из БД.
    Отличается от APIVIEW тем что количество строк кода меньше а функционал такой же.
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializerSet

    def create(self, request, *args, **kwargs):
        """
        Этот метод отвечает за создание новой записи.
        :param request:
        :param args:
        :param kwargs:
        :return: id новой записи.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Сохранение объекта
            self.perform_create(serializer)
            data = Delivery.objects.order_by('id').last()
            data = model_to_dict(data)
            return Response({"new_order":data['id']})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Метод отвечает за обновление записи в таблице заказов из БД.
        :param request:
        :param args:
        :param kwargs:
        :return: Новые данные.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = model_to_dict(serializer.data)
        return Response({"update_order":data})

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    # Отображается поле поиска.
    search_fields = ['id', 'delivery_city', 'package_type', 'customer_name']

    # Отображается поле фильтрации.
    filterset_fields = [
        'id',
        'package_type',
        'delivery_city',
        'customer_name'
    ]
    # Отображается поле сортировки.
    ordering_fields = [
        'id',
        'delivery_city',
        'package_type',
        'customer_name'
    ]
