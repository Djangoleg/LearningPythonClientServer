"""Программа-клиент"""
import logging
import sys
import json
import socket
import time
from os import system

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, LOGGER_NAME_CLIENT, DEFAULT_CLIENT_MODE, SENDER, MESSAGE_TEXT, \
    MESSAGE
from common.utils import get_message, send_message

from  log.config_client_log import client_logger
from log.decorator_log import Log

logger = logging.getLogger(LOGGER_NAME_CLIENT)

class Client:

    @Log()
    def __init__(self):
        '''
        Инициализация параметров коммандной строки
        client.py 192.168.1.2 8079
        '''
        try:
            server_address = sys.argv[1]
            server_port = int(sys.argv[2])
            client_mode = sys.argv[3]
            window_title = sys.argv[4]
            system("title " + window_title)

            if server_port < 1024 or server_port > 65535:
                raise ValueError('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')

            if client_mode not in ('listen', 'send'):
                raise ValueError(f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')

            self.client_settings = (server_address, server_port)
            self.client_mode = client_mode

        except Exception as e:
            self.client_settings = (DEFAULT_IP_ADDRESS, DEFAULT_PORT)
            self.client_mode = DEFAULT_CLIENT_MODE

    @Log()
    def get_transport(self):
        # Инициализация сокета и обмен
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect(self.client_settings)

        return transport

    @Log()
    def message_from_server(self, message):
        """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
        if ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and MESSAGE_TEXT in message:
            print(f'Получено сообщение от пользователя '
                  f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            logger.info(f'Получено сообщение от пользователя '
                        f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        else:
            logger.error(f'Получено некорректное сообщение с сервера: {message}')

    @Log()
    def create_message(self, sock, account_name='Guest'):
        """Функция запрашивает текст сообщения и возвращает его.
        Так же завершает работу при вводе подобной комманды
        """
        message = input('Введите сообщение для отправки или \'stop\' для завершения работы: ')
        if message == 'stop':
            sock.close()
            logger.info('Завершение работы по команде пользователя.')
            print('Спасибо за использование нашего сервиса!')
            sys.exit(0)
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: account_name,
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        return message_dict

    @Log()
    def create_presence(self, account_name='Guest'):
        '''
        Функция генерирует запрос о присутствии клиента
        :param account_name:
        :return:
        '''
        # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        return out

    @Log()
    def process_answer(self, message):
        '''
        Функция разбирает ответ сервера
        :param message:
        :return:
        '''
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ValueError

    @Log()
    def process_message(self, account_name):

        if self.client_mode == 'send':
            print(f'Имя пользователя: {account_name}. Режим работы - отправка сообщений.')
        else:
            print(f'Имя пользователя: {account_name}. Режим работы - приём сообщений.')

        transport = self.get_transport()

        try:
            message_to_server = self.create_presence(account_name)
            send_message(transport, message_to_server)
            answer = self.process_answer(get_message(transport))
            logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
            print(f'Установлено соединение с сервером.')

        except (ValueError, json.JSONDecodeError):
            logger.error('Не удалось декодировать сообщение сервера.')
            sys.exit(1)

        while True:
            if self.client_mode == 'send':
                try:
                    send_message(transport, self.create_message(transport, account_name))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {self.client_settings[0]} было потеряно.')
                    sys.exit(1)

            if self.client_mode == 'listen':
                try:
                    self.message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {self.client_settings[0]} было потеряно.')
                    sys.exit(1)

if __name__ == '__main__':
    account_name = 'Super man'
    client = Client()
    client.process_message(account_name)

