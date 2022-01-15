"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import glob

FILE_MASK = 'info*.txt'


def get_data():
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    file_count = 0
    for file in glob.glob(FILE_MASK):
        # print(file)
        file_count += 1
        with open(file, encoding='utf-8') as f_n:
            for line in f_n:
                if main_data[0][0] in line:
                    os_prod_list.append(line.strip().split(':')[1].strip())
                elif main_data[0][1] in line:
                    os_name_list.append(line.strip().split(':')[1].strip())
                elif main_data[0][2] in line:
                    os_code_list.append(line.strip().split(':')[1].strip())
                elif main_data[0][3] in line:
                    os_type_list.append(line.strip().split(':')[1].strip())

    for x in range(file_count):
        main_data.append([os_prod_list[x], os_name_list[x], os_code_list[x], os_type_list[x]])

    return main_data


def write_to_csv(file_path):
    data_to_csv = get_data()
    with open(file_path, "w", newline='', encoding='utf-8') as f_n:
        F_N_WRITER = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        for row in data_to_csv:
            F_N_WRITER.writerow(row)


file_name = 'data_report_new.csv'
write_to_csv(file_name)
