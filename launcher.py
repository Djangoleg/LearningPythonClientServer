"""Лаунчер"""

import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py -a 127.0.0.1 -p 7778',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROCESS.append(subprocess.Popen(f'python client.py 127.0.0.1 7778 user_{i}',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
