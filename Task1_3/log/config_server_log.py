import sys
import os
import logging.handlers
from common.variables import LOGGING_LEVEL, LOGS_DIR, FILE_NAME_SERVER_LOG


def get_server_logger():
    # Формат вывода лога.
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

    # Путь к файлу лога.
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) + LOGS_DIR, FILE_NAME_SERVER_LOG)

    # Вывод лога в файл.
    log_file = logging.handlers.TimedRotatingFileHandler(log_file_path, encoding='utf8', interval=1, when='D')
    log_file.setFormatter(log_formatter)

    # создаём регистратор и настраиваем его
    server_logger = logging.getLogger('server')
    server_logger.addHandler(log_file)
    server_logger.setLevel(LOGGING_LEVEL)

    return server_logger

# отладка
if __name__ == '__main__':
    logger = get_server_logger()
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
