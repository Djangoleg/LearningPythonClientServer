import sys
import os
import logging
from common.variables import LOGGING_LEVEL, LOGS_DIR, FILE_NAME_CLIENT_LOG


def get_client_logger():
    # Формат вывода лога.
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

    # Путь к файлу лога.
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) + LOGS_DIR, FILE_NAME_CLIENT_LOG)

    # Вывод лога в файл.
    log_file = logging.FileHandler(log_file_path, encoding='utf8')
    log_file.setFormatter(log_formatter)

    # Создаём регистратор и настраиваем его
    client_logger = logging.getLogger('client')
    client_logger.addHandler(log_file)
    client_logger.setLevel(LOGGING_LEVEL)

    return  client_logger

if __name__ == '__main__':
    logger = get_client_logger()
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
