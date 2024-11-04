"""
The main module.
"""

from datetime import datetime

import config
from config import CURR_LANG

from get_data import get_rows
from logger import get_my_logger


def get_process_date() -> tuple[datetime | None, datetime | None] :
    '''
    Requesting and receiving from the user the date for which the processing will be performed
    :return: A tuple of two timestamps indicating the beginning and end of the processing time interval
             or <None> in case of a failed attempt
    '''
    while True:
        start_time, end_time = None, None
        str_date = input(config.AN_INVITATION_FOR_ENTERING_PROCESSING_DATE[CURR_LANG])
        if str_date.lower() == 'exit': break
        try:
            start_time = datetime.fromisoformat(str_date + ' 00:00:00.000000')
            end_time = datetime.fromisoformat(str_date + ' 23:59:59.999999')
            break
        except ValueError:
            print(config.MESSAGE_ABOUT_BAD_INPUT[CURR_LANG])
            continue

    return start_time, end_time


def main():
    # The main function
    #
    # Requesting a processing date
    start_time, end_time = get_process_date()
    if start_time is not None:
        # Initialize our logger
        my_logger, _ = get_my_logger()
        my_logger.info(config.LOG_STARTING_WORK_WITH_API[CURR_LANG])
        # Getting the lines
        # rows = get_rows(my_logger, start_time=start_time, end_time=end_time)
        my_logger.info(config.LOG_ENDING_WORK_WITH_API[CURR_LANG])
        # Putting information to the database
        my_logger.info(config.LOG_STARTING_WORK_WITH_DBMS[CURR_LANG])
        # put_in_base(my_logger, rows)
        my_logger.info(config.LOG_ENDING_WORK_WITH_DBMS[CURR_LANG])


if __name__ == '__main__':
    main()