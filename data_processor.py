"""
The main module.
"""

from datetime import date, time, datetime

# App's modules
import config
from config import CURR_LANG
from get_data import get_rows
from put_data import put_in_base, create_database_connection, DatabaseConnection
from logger import Mylogger
from google_sheets import create_google_sheets_report
from email_notifications import send_email_notifications


# # Language package of service messages
AN_INVITATION_FOR_ENTERING_PROCESSING_DATE = (
    'Введите дату извлечения/загрузки данных в формате: <YYYY-mm-dd> или <exit> для выхода: ',
    'Enter processing date in format: <<YYYY-mm-dd> or type <exit> for quit: '
)
MESSAGE_ABOUT_BAD_INPUT = (
    'Ошибка ввода даты, попробуйте еще раз...',
    'Bad input. Let\'s try again...'
)


def get_process_date() -> date | None :
    '''
    Requesting and receiving from the user the date for which the processing will be performed
    :return: A processing date or <None> in case of a failed attempt
    '''
    while True:
        process_date = None
        str_date = input(AN_INVITATION_FOR_ENTERING_PROCESSING_DATE[CURR_LANG.value])
        if str_date.lower() == 'exit' :
            break
        try:
            process_date = date.fromisoformat(str_date)
            break
        except ValueError:
            print(MESSAGE_ABOUT_BAD_INPUT[CURR_LANG.value])
            continue

    return process_date


def main_conveyor(process_date: date, test_mode: bool) -> None :
    '''
    The main function.
    :param process_date: the date on which the processing is performed
    :param test_mode: if it's True will be performed only processing for first hour entered date
    :return: None
    '''

    # Initialize our logger
    logger = Mylogger(process_date)

    # Processing the date in the selected mode (full date or one first hour)
    start_time = datetime.combine(process_date, time(0, 0, 0, 0))
    end_time = datetime.combine(process_date, time(0 if test_mode else 23, 59, 59, 999999))

    # Getting the lines
    rows = get_rows(logger, start_time, end_time)

    # The starting mark in the log about loading data in database
    logger.msg_dbms_start_work()
    # Creating the instance of DatabaseConnection class
    db_connection: DatabaseConnection = create_database_connection(logger)
    
    if db_connection is not None:
        # Putting information to the database
        result : bool = put_in_base(logger, db_connection, rows)

        if not result :
            return

        # Create Google sheets report
        googl_sheets_result : bool = create_google_sheets_report(logger, db_connection, process_date)
        db_connection.close()

        # sending email notifications
        send_email_notifications(logger, process_date, googl_sheets_result)


if __name__ == '__main__':
    # Requesting a processing date
    process_date : date | None = get_process_date()
    if process_date is not None:
        main_conveyor(process_date, test_mode=config.TEST_APP_MODE)
