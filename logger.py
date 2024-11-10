"""
The module for working with logging of application data processing
"""

from datetime import datetime
import re
import os
import logging

# App's modules
import config
from exceptions import ErrorInitLogsStorage


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


if __name__ == '__main__' :
    logger, log_file = get_my_logger('My_logger')
    logger.info(f'test for - {log_file}')
