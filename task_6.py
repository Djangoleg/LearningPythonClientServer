"""
Задание 6.

Создать  НЕ программно (вручную) текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».

Принудительно программно открыть файл в формате Unicode и вывести его содержимое.
Что это значит? Это значит, что при чтении файла вы должны явно указать кодировку utf-8
и файл должен открыться у ЛЮБОГО!!! человека при запуске вашего скрипта.

При сдаче задания в папке должен лежать текстовый файл!

Это значит вы должны предусмотреть случай, что вы по дефолту записали файл в cp1251,
а прочитать пытаетесь в utf-8.

Преподаватель будет запускать ваш скрипт и ошибок НЕ ДОЛЖНО появиться!

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО!!! в формате Unicode (utf-8)
--- обратите внимание на чтение файла в режиме rb
для последующей переконвертации в нужную кодировку

НАРУШЕНИЕ обозначенных условий - задание не выполнено!!!
"""
import chardet as chardet

file_name = 'test_file.txt'

# words = ['сетевое программирование', 'сокет', 'декоратор']
# with open(file_name, 'w', encoding='utf-8') as file:
#     for line in words:
#         file.write(line + '\n')


def convert_file_encoding():
    with open(file_name, 'rb') as test_file:
        raw_data = test_file.read()
    chardet_result = chardet.detect(raw_data)
    encoding = chardet_result['encoding']
    content_text = raw_data.decode(encoding)
    with open(file_name, 'w', encoding='utf-8') as test_file:
        test_file.write('\n'.join(content_text.splitlines()))


convert_file_encoding()

with open(file_name, 'r', encoding='utf-8') as f:
    data = f.read()
print(data)
