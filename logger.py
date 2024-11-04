# модуль работы с логированием обработки данных приложения

from datetime import datetime
import re
import os
import logging

# импорт из модулей приложения
import config
from exceptions import ErrorInitLogsStorage


def init_log_storage(path: str) -> str | None :
    '''
    Функция подготовки файловой инфраструктуры логирования
    :param path: папка для хранения логов
    :return: полное имя файла логирования в случае успешной настройки и None в случае ошибки
    '''
    try :
        new_log_name = datetime.now().strftime('%Y-%m-%d_%H-%M') + '.log'

        if not os.path.isdir(path) :
            # если папки логов нет, создаем её
            os.mkdir(path)
        else :
            # читаем содержимое папки логов
            list_dir = os.listdir(path)
            # вычисляем re-шаблон имени лога
            regexp = re.compile(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log')
            # отбираем все файлы-логи
            list_logs = []
            for el in list_dir :
                if regexp.match(el, 0) :
                    list_logs.append(el)
            # сортируем в порядке "возраста" лога
            list_logs.sort(reverse=True)
            if new_log_name in list_logs[:config.MAX_NUM_LOGS_FILES] :
                start_pos = config.MAX_NUM_LOGS_FILES
            else :
                start_pos = config.MAX_NUM_LOGS_FILES - 1
            if list_logs[start_pos:] :
                for f in list_logs[start_pos:] :
                    os.remove(os.path.join(path, f))

        return os.path.join(path, new_log_name)

    except Exception :
        return None


def get_my_logger(name: str = 'root',
                  level: str = logging.INFO,
                  path: str = config.LOGS_PATH) -> tuple[logging.Logger, str] :
    '''
    Функция инициализации пользовательского логгера
    :param name: имя логгера (по умолчанию - 'root')
    :param level: уровень логирования (по умолчанию - 'root')
    :param path: путь к папке логов (по умолчанию - 'root')
    :return: объект класса logging.Logger
    '''

    full_name_file_log = init_log_storage(path)
    if not full_name_file_log :
        raise ErrorInitLogsStorage
    else :
        # создаем регистратор
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # создаем обработчик для файла
        handler = logging.FileHandler(full_name_file_log, mode='w')
        # строка формата сообщения
        msg_fmt = '[%(name)s] [%(asctime)s] [%(levelname)s] > %(message)s'
        # строка формата времени
        date_fmt = '%Y-%m-%d %H:%M:%S'
        # создаем форматтер
        formatter = logging.Formatter(fmt=msg_fmt, datefmt=date_fmt)
        # добавление форматтера к обработчику
        handler.setFormatter(formatter)
        # добавление обработчика к логгеру
        logger.addHandler(handler)
    return logger, full_name_file_log


if __name__ == '__main__' :
    logger, log_file = get_my_logger('My_logger')
    logger.info(f'test for - {log_file}')
