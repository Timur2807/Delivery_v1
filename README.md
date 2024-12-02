Добро пожаловать в этот проект!
В этом проекте реализовано API для обработки заказов.
Функционал API в себя включать возможность создать заявку, обновить заявку, получить статус по заявке, завершить заявку. 
Данные фиксируются в БД.
В приложении my_app реализовано джанго команды в папке management/commands/...
В модуле my_app/models.py представлены модели заказа, статуса и истории статусов. 
В модуле my_app/serializers.py представлены классы серализаторы DeliverySerializerSet для ModelViewSet и DeliverySerializer для APIView
В модуле my_app/urls.py представлены ссылки для представления записей из БД.
В модуле delivery/urls.py представлены ссылки  на документацию.
В модуле my_app/views.py представлены классы, которые взаимодействуют с БД и обрабатывают различные запросы. 
В модуле delivery/quieries.sql представлены запросы в БД на языке SQL.
