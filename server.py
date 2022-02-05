import logging
import select
import socket
import sys
import json
import time

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, LOGGER_NAME_SERVER, MESSAGE, SENDER, MESSAGE_TEXT
from common.utils import get_message, send_message

from  log.config_server_log import server_logger
from log.decorator_log import Log

logger = logging.getLogger(LOGGER_NAME_SERVER)

class Server:

    @Log()
    def __get_settings(self):
        '''
       Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
       Сначала обрабатываем порт:
       server.py -p 8079 -a 192.168.1.2
       :return:
       '''
        try:
            if '-p' in sys.argv:
                listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            else:
                listen_port = DEFAULT_PORT
            if listen_port < 1024 or listen_port > 65535:
                raise ValueError
        except IndexError:
            logger.error('После параметра -\'p\' необходимо указать номер порта.')
            sys.exit(1)
        except ValueError:
            logger.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        # Затем загружаем какой адрес слушать.
        try:
            if '-a' in sys.argv:
                listen_address = sys.argv[sys.argv.index('-a') + 1]
            else:
                listen_address = ''

        except IndexError:
            logger.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            sys.exit(1)

        return (listen_address, listen_port)

    @Log()
    def process_client_message(self, message, messages_list, client):
        """
        Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
        проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
        :param message:
        :param messages_list:
        :param client:
        :return:
        """
        logger.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем, если успех
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] != '':
            send_message(client, {RESPONSE: 200})
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and \
                TIME in message and MESSAGE_TEXT in message:
            messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        # Иначе отдаём Bad request
        else:
            send_message(client, {
                RESPONSE: 400,
                ERROR: 'Bad Request'
            })

    @Log()
    def start(self):

        server_settings = self.__get_settings()

        # Готовим сокет.
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind(server_settings)
        transport.settimeout(0.5)

        logger.info(f'Start local server on port: {server_settings[1]}')

        # Слушаем порт.
        transport.listen(MAX_CONNECTIONS)

        # Список клиентов, очередь сообщений.
        clients = []
        messages = []

        while True:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = transport.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соедение с клиентом: {client_address}')
                print(f'Установлено соедение с клиентом: {client_address}')
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов.
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если там есть сообщения,
            # кладём в словарь, если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        client_message = get_message(client_with_message)
                        print(f'Получено сообщение от клиента: {client_message}')
                        self.process_client_message(client_message, messages, client_with_message)
                    except:
                        logger.info(f'Клиент {client_with_message.getpeername()} '
                                    f'отключился от сервера.')
                        clients.remove(client_with_message)

            # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
            if messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: messages[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: messages[0][1]
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        print(f'Отправка сообщения: {message} клиенту: {waiting_client.getpeername()}')
                        send_message(waiting_client, message)
                    except:
                        logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                        clients.remove(waiting_client)


if __name__ == '__main__':
    server = Server()
    server.start()
