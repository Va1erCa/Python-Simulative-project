"""
The module for working with logging of application data processing
"""

from datetime import datetime, date
import re
import os
import logging

# App's modules
import config
from exceptions import ErrorInitLogsStorage
from app_types import Language, Row


def _init_log_storage(path: str) -> str | None :
    '''
    The function of preparing the logging files infrastructure
    :param path: folder for storing logs
    :return: the full name of the logging file in case of successful configuration and <None> in case of an error
    '''

    try :
        new_log_name = datetime.now().strftime('%Y-%m-%d_%H-%M') + '.log'

        if not os.path.isdir(path) :
            # Creating a log folder if it doesn't exist yet
            os.mkdir(path)
        else :
            # Reading a log folder
            list_dir = os.listdir(path)
            # Compiling "re"-pattern for the name of log
            regexp = re.compile(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log')
            # Finding all of logs files
            list_logs = []
            for el in list_dir :
                if regexp.match(el, 0) :
                    list_logs.append(el)
            # Sorting the log list by file creation time in reverse order
            list_logs.sort(reverse=True)
            if new_log_name in list_logs[:config.MAX_NUM_LOGS_FILES] :
                start_pos = config.MAX_NUM_LOGS_FILES
            else :
                start_pos = config.MAX_NUM_LOGS_FILES - 1
            if list_logs[start_pos :] :
                for f in list_logs[start_pos :] :
                    os.remove(os.path.join(path, f))

        return os.path.join(path, new_log_name)

    except Exception :
        return None


def _get_my_logger(name: str = 'root',
                   level: str = logging.INFO,
                   path: str = config.LOGS_PATH) -> tuple[logging.Logger, str] :
    '''
    Function of creating and initializing custom's logger.
    :param name: logger's name (by default - 'root')
    :param level: logging level (by default - logging.INFO)
    :param path: path to logs folder (by default it is equal a constant - LOGS_PATH from config.py file)
    :return: a tuple including an instance of the class "logging.Logger" and a full name of log file
    '''

    full_name_file_log = _init_log_storage(path)
    if not full_name_file_log :
        raise ErrorInitLogsStorage
    else :
        # Creating logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # Creating handler
        handler = logging.FileHandler(full_name_file_log, mode='w')
        # Format-string for log message
        msg_fmt = '[%(name)s] [%(asctime)s] [%(levelname)s] > %(message)s'
        # Format-string for date-time
        date_fmt = '%Y-%m-%d %H:%M:%S'
        # Creating a formatter
        formatter = logging.Formatter(fmt=msg_fmt, datefmt=date_fmt)
        # Adding a formatting tool to the handler
        handler.setFormatter(formatter)
        # Adding a handler to the logger
        logger.addHandler(handler)
    return logger, full_name_file_log


class Mylogger() :
    def __init__(self,
                 process_date : date,
                 name: str = 'root',
                 level: int = logging.INFO,
                 path: str = config.LOGS_PATH,
                 language: Language = config.CURR_LANG) -> None:

        self._name = name
        self._level = level
        self._logger, self.full_name_file_log = _get_my_logger(name, level, path)
        self._language = language
        self._process_date = process_date

    # Methods for creating logger messages
    def msg(self, level: int, message: str, *args, **kwargs) -> None:
        self._logger.log(self._level, message, *args, **kwargs)

    def msg_api_start_work(self, start_time: datetime, end_time:datetime) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(self._level, f'начинаем сбор данных за {self._process_date} '
                                      f'с: {start_time} по: {end_time}')
            case Language.ENGLISH :
                self.msg(self._level, f'we start collecting data for {self._process_date} '
                                      f'from: {start_time} to: {end_time}')

    def msg_api_row_was_read(self, num_row: int, row: Row) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(self._level, f'строка № {num_row} прочитана: {row}')
            case Language.ENGLISH :
                self.msg(self._level, f'line # {num_row} was read: {row}')

    def msg_api_row_was_error_read(self, num_row: int) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(self._level, f'строка № {num_row} не прочитана - ошибка - '
                                      f'отсутствует идентификатор <lti_user_id>')
            case Language.ENGLISH :
                self.msg(self._level, f'line # {num_row} wasn\'t read - error - '
                                      f'the <lti_user_id> id is missing')

    def msg_api_end_work(self, total_readed: int, corrupt_readed: int) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(self._level, f'завершено скачивание данных за {self._process_date}')
                self.msg(self._level, f'общее количество прочитанных строк: {total_readed}, '
                                      f'в том числе {total_readed - corrupt_readed} успешно, '
                                      f'{corrupt_readed} испорчено')
            case Language.ENGLISH :
                self.msg(self._level, f'data download completed for {self._process_date}')
                self.msg(self._level, f'total number of lines read: {total_readed}, '
                                      f'including {total_readed - corrupt_readed} successfully, '
                                      f'{corrupt_readed} is corrupted')

    def msg_dbms_start_work(self) -> None:
        match self._language :
            case Language.RUSSIAN :
                self.msg(self._level,f'загрузка данных в базу началась')
            case Language.ENGLISH :
                self.msg(logging.ERROR,f'the upload to the database has started')

    def msg_creating_database_connection_error(self, error: object) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(logging.ERROR,f'Ошибка создания экземпляра класса подключения к базе данных: {error}')
            case Language.ENGLISH :
                self.msg(logging.ERROR,f'DatabaseConnection instance creating error: {error}')

    def msg_main_table_init_error(self, error: object) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(logging.ERROR, f'Ошибка инициализации главной таблицы базы данных: {error}')
            case Language.ENGLISH :
                self.msg(logging.ERROR, f'Error initializing the main database table: {error}')

    def msg_omission_or_incorrect_data(self, line: int, error: str) -> None:
        match self._language :
            case Language.RUSSIAN :
                error = error.replace('#', ' пропущено значение поля: ')
                error = error.replace('$', ' некорректное сочетание значений полей: ')
                self.msg(logging.ERROR, f'строка {line} есть ошибки:{error}')
            case Language.ENGLISH :
                error = error.replace('#', ' value of the field is missing: ')
                error = error.replace('$', ' incorrect combination of parameters: ')
                self.msg(logging.ERROR, f'line {line} there are errors:{error}')

    def msg_dbms_end_work(self, total_writed: int, defect_writed: int ) -> None :
        match self._language :
            case Language.RUSSIAN :
                self.msg(self._level, f'загрузка данных в базу завершена')
                self.msg(self._level, f'общее количество добавленных строк: {total_writed}, '
                                      f'в том числе {defect_writed} с дефектами')
            case Language.ENGLISH :
                self.msg(self._level, f'the upload to the database has ended')
                self.msg(self._level, f'total number of added lines: {total_writed}, '
                                      f'including {defect_writed} with defects')


if __name__ == '__main__' :
    logger = Mylogger(date(2024, 10, 1))
    logger.msg(logger._le.ng.INFO, f'test for - {logger.full_name_file_log}')
