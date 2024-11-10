"""
The main module.
"""

from datetime import date, time, datetime

# App's modules
import config
from config import CURR_LANG
from get_data import get_rows
from put_data import init_data_base
from logger import get_my_logger


def get_process_date() -> date | None :
    '''
    Requesting and receiving from the user the date for which the processing will be performed
    :return: A tuple of two timestamps indicating the beginning and end of the processing time interval
             or <None> in case of a failed attempt
    '''
    while True:
        process_date = None
        str_date = input(config.AN_INVITATION_FOR_ENTERING_PROCESSING_DATE[CURR_LANG])
        if str_date.lower() == 'exit' :
            break
        try:
            process_date = date.fromisoformat(str_date)
            break
        except ValueError:
            print(config.MESSAGE_ABOUT_BAD_INPUT[CURR_LANG])
            continue

    return process_date


def main_conveyor(process_date: date, test_mode: bool = False) -> None :
    '''
    The main conveyor function.
    :param process_date: the date for which the processing is performed
    :param test_mode: if it's True will be performed only processing for first hour entered date
    :return: None
    '''

    # Initialize our logger
    my_logger, _ = get_my_logger()

    # Processing the date in the selected mode (full date or one first hour)
    #
    start_time = datetime.combine(process_date, time(0, 0, 0, 0))
    end_time = datetime.combine(process_date, time(0 if test_mode else 23, 59, 59, 999999))

    # The starting mark in the log for api-working with selected time interval
    my_logger.info(f'{config.LOG_STARTING_WORK_WITH_API[CURR_LANG][0]}{process_date}'
                   f'{config.LOG_STARTING_WORK_WITH_API[CURR_LANG][1]}{start_time}'
                   f'{config.LOG_STARTING_WORK_WITH_API[CURR_LANG][2]}{end_time}'
                   )

    # Getting the lines and statistic
    rows, total_lines_read, corrupt_read = get_rows(my_logger, start_time=start_time, end_time=end_time)

    # The ending mark in the log for api-working with date
    my_logger.info(f'{config.LOG_ENDING_WORK_WITH_API[CURR_LANG]}{process_date}')
    my_logger.info(f'{config.LOG_TOTAL_NUM_LINES_API[CURR_LANG][0]}{total_lines_read}'
                   f'{config.LOG_TOTAL_NUM_LINES_API[CURR_LANG][1]}{total_lines_read - corrupt_read}'
                   f'{config.LOG_TOTAL_NUM_LINES_API[CURR_LANG][2]}{corrupt_read}'
                   f'{config.LOG_TOTAL_NUM_LINES_API[CURR_LANG][3]}'
                   )

    # Putting information to the database
    my_logger.info(config.LOG_STARTING_WORK_WITH_DBMS[CURR_LANG])
    my_connection = init_data_base(my_logger)
    if my_connection is not None :
        # put_in_base(my_logger, rows)
        ...
    my_logger.info(config.LOG_ENDING_WORK_WITH_DBMS[CURR_LANG])


if __name__ == '__main__':
    # Requesting a processing date
    process_date = get_process_date()
    if process_date is not None:
        main_conveyor(process_date, test_mode=config.TEST_APP_MODE)
