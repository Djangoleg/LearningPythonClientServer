"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "принтер", (возможные проблемы с кирилицей)
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""
import json

json_file = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    order_item = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    json_dict = dict()
    with open(json_file, encoding='utf-8') as f_n:
        json_content = f_n.read()
        json_dict = json.loads(json_content)

    orders = json_dict.get("orders", list())
    orders.append(order_item)
    json_dict["orders"] = orders

    with open(json_file, 'w', encoding='utf-8') as f_n:
        json.dump(json_dict, f_n, sort_keys=True, indent=4, ensure_ascii=False)


orders_list = [
    {
        "item": "принтер",
        "quantity": "10",
        "price": "6700",
        "buyer": "Ivanov I.I.",
        "date": "24.09.2017"
    },
    {
        "item": "scaner",
        "quantity": "20",
        "price": "10000",
        "buyer": "Petrov P.P.",
        "date": "11.01.2018"
    },
    {
        "item": "scaner",
        "quantity": "20",
        "price": "10000",
        "buyer": "Petrov P.P.",
        "date": "11.01.2018"
    },
    {
        "item": "scaner",
        "quantity": "20",
        "price": "10000",
        "buyer": "Petrov P.P.",
        "date": "11.01.2018"
    }
]

for item in orders_list:
    item_list = list()
    for key, val in item.items():
        item_list.append(val)

    print(*item_list)
    write_order_to_json(*item_list)
    item_list = list()

with open(json_file, encoding='utf-8') as f_n:
    print(f_n.read())
