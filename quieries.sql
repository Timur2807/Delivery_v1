
---Количество успешно завершенных заказов И их среднее время выполнения в разрезе городов.
SELECT d.delivery_city, COUNT(ds.id) AS completed_count,
AVG(EXTRACT(EPOCH FROM ds.load_data AT TIME ZONE 'UTC') / 60) AS average_duration
FROM my_app_deliverystatuscurrent ds
LEFT JOIN my_app_delivery d ON ds.delivery_id = d.id
WHERE ds.status_name = 'Done'
GROUP BY d.delivery_city;
-- результат
[
{
'city': 'Набережные Челны',
'completed_count': 128,
'average_duration': '12:19:00'
},
{
'city': 'Зеленодольск',
'completed_count': 28,
'average_duration': '12:05:00'
},
{
'city': 'Нижнекамск',
'completed_count': 106,
'average_duration': '12:51:00'
},
{
'city': 'Альметьевск',
'completed_count': 52,
'average_duration': '12:47:00'
},
{
'city': ' г Набережные Челны',
'completed_count': 1,
'average_duration': '23:37:00'
},
{
'city': 'Казань',
'completed_count': 147,
'average_duration': '11:41:00'
}
]


--    Количество заявок в разрезе статусов,
--    которые поступили за последние 3 недели с типом доставки «Письмо» и «Бандероль»

SELECT my_app_deliverystatuscurrent.status_name, COUNT(my_app_deliverystatuscurrent.id) AS "count"
FROM my_app_deliverystatuscurrent
INNER JOIN my_app_delivery ON (my_app_deliverystatuscurrent.delivery_id = my_app_delivery.id)
WHERE my_app_delivery.delivery_date BETWEEN '2024-07-19' AND '2024-09-08'
	AND my_app_delivery.package_type IN ('Письмо', 'Бандероль')
GROUP BY my_app_deliverystatuscurrent.status_name
ORDER BY my_app_deliverystatuscurrent.status_name ASC;
-- можно попробовать с LEFT JOIN
-- результат
-- Статус: Cancelled, Количество: 6
-- Статус: Done, Количество: 38
-- Статус: Handed to courier, Количество: 15
-- Статус: In Progress, Количество: 6
-- Статус: New, Количество: 15


--3. Среднее время нахождение заявки на каждом этапе в городе Казань в разрезе типа посылки для завершенных заявок.
SELECT my_app_delivery.package_type,my_app_deliverystatushistory.status_name,
       AVG((my_app_deliverystatushistory.load_data - my_app_delivery.load_data)) AS average_duration
FROM my_app_deliverystatushistory
INNER JOIN my_app_delivery ON my_app_deliverystatushistory.delivery_id = my_app_delivery.id
WHERE (my_app_deliverystatushistory.delivery_id IN (SELECT dlv."id"
                                                        FROM my_app_delivery AS dlv
                                                        LEFT OUTER JOIN my_app_deliverystatuscurrent AS stc ON (dlv.id = stc.delivery_id)
                                                        WHERE dlv.delivery_city = 'Казань') AND my_app_deliverystatushistory.status_name IN ('Done', 'Cancelled'))
GROUP BY my_app_delivery.package_type, my_app_deliverystatushistory.status_name;

-- результат
-- Тип посылки: Габаритный груз, Статус: Done, Среднее время: 2 days, 3:07:35.886364
-- Тип посылки: Бандероль, Статус: Cancelled, Среднее время: 2 days, 0:08:23.571428
-- Тип посылки: Габаритный груз, Статус: Cancelled, Среднее время: 2 days, 15:47:10.833333
-- Тип посылки: Письмо, Статус: Done, Среднее время: 1 day, 23:53:41.986842
-- Тип посылки: Бандероль, Статус: Done, Среднее время: 2 days, 6:17:09.965517
-- Тип посылки: Письмо, Статус: Cancelled, Среднее время: 2 days, 6:40:23.600000




