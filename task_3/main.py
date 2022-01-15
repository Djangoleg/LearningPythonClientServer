"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml

yaml_file_name = 'test_file.yaml'

phone_dict_in = {'brands': ['apple', 'samsung', 'one plus', 'xiaomi', 'lg'],
           'quantity': 50,
           'price': {'apple': '1000€-2000€',
                     'samsung': '400€-1500€',
                     'one plus': '400€-1500€',
                     'xiaomi': '200€-1500€',
                     'lg': '200€-1500€'}
                 }

with open(yaml_file_name, 'w', encoding='utf-8') as file:
    yaml.dump(phone_dict_in, file, default_flow_style=False, allow_unicode=True, sort_keys=False
              )

with open(yaml_file_name, 'r', encoding='utf-8') as file:
    phone_dict_out = yaml.load(file, Loader=yaml.SafeLoader)

print(phone_dict_in.__eq__(phone_dict_out))
