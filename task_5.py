"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import subprocess
import chardet as chardet

args_list = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]

for args in args_list:
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        chardet_result = chardet.detect(line)
        encoding = chardet_result['encoding']
        print(line.decode(encoding))




